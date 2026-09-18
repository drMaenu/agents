from app.models.chat_models import ChatMessage, ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.topic_guard import SUPPORT_REJECTION_MESSAGE
from app.models.chat_models import ChatMessage
from app.services.escalation_guard import ESCALATION_MESSAGE


class DummyAgent:
    def __init__(self) -> None:
        self.called = False
        self.last_request = None

    def get_response(self, request: ChatRequest) -> ChatResponse:
        self.called = True
        self.last_request = request
        return ChatResponse(
            answer="Support-Antwort",
            model="dummy-agent",
        )


def test_process_chat_allows_support_request():
    agent = DummyAgent()
    service = ChatService(agent=agent)

    request = ChatRequest(message="Mein WLAN funktioniert nicht.")
    response = service.process_chat(request)

    assert response.answer == "Support-Antwort"
    assert response.model == "dummy-agent"
    assert agent.called is True


def test_process_chat_rejects_off_topic_request_without_agent_call():
    agent = DummyAgent()
    service = ChatService(agent=agent)

    request = ChatRequest(message="Schreibe mir ein Gedicht über den Sommer.")
    response = service.process_chat(request)

    assert response.answer == SUPPORT_REJECTION_MESSAGE
    assert response.model == "topic-guard"
    assert agent.called is False


def test_process_chat_preserves_history_for_agent():
    agent = DummyAgent()
    service = ChatService(agent=agent)

    request = ChatRequest(
        message="Fehler 403 beim Login.",
        history=[
            ChatMessage(role="user", content="Ich kann mich nicht anmelden."),
            ChatMessage(role="assistant", content="Welche Fehlermeldung wird angezeigt?"),
        ],
    )

    response = service.process_chat(request)

    assert response.answer == "Support-Antwort"
    assert response.model == "dummy-agent"
    assert agent.called is True
    assert agent.last_request is not None
    assert agent.last_request.message == "Fehler 403 beim Login."
    assert len(agent.last_request.history) == 2
    assert agent.last_request.history[0].content == "Ich kann mich nicht anmelden."
    assert agent.last_request.history[1].content == "Welche Fehlermeldung wird angezeigt?"


def test_process_chat_allows_follow_up_with_support_context():
    agent = DummyAgent()
    service = ChatService(agent=agent)

    request = ChatRequest(
        message="HP LaserJet",
        history=[
            ChatMessage(role="user", content="Mein Drucker funktioniert nicht."),
            ChatMessage(role="assistant", content="Welches Modell ist es?"),
        ],
    )

    response = service.process_chat(request)

    assert response.answer == "Support-Antwort"
    assert response.model == "dummy-agent"
    assert agent.called is True


def test_process_chat_returns_escalation_without_agent_call():
    agent = DummyAgent()
    service = ChatService(agent=agent)

    request = ChatRequest(message="Bitte Ticket erstellen, ich habe alles probiert.")
    response = service.process_chat(request)

    assert "Dieses Anliegen sollte an den nächsten Support-Level weitergegeben werden." in response.answer
    assert "- Aktuelle Anfrage: Bitte Ticket erstellen, ich habe alles probiert." in response.answer
    assert "- Eskalationsgrund:" in response.answer
    assert response.model == "escalation-guard"
    assert agent.called is False