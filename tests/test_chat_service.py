from app.models.chat_models import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.topic_guard import SUPPORT_REJECTION_MESSAGE


class DummyAgent:
    def __init__(self) -> None:
        self.called = False

    def get_response(self, request: ChatRequest) -> ChatResponse:
        self.called = True
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

def test_process_chat_allows_login_problem():
    agent = DummyAgent()
    service = ChatService(agent=agent)

    request = ChatRequest(message="Ich kann mich nicht anmelden.")
    response = service.process_chat(request)

    assert response.answer == "Support-Antwort"
    assert response.model == "dummy-agent"
    assert agent.called is True

def test_process_chat_rejects_recipe_request_without_agent_call():
    agent = DummyAgent()
    service = ChatService(agent=agent)

    request = ChatRequest(message="Wie koche ich Lasagne?")
    response = service.process_chat(request)

    assert response.answer == SUPPORT_REJECTION_MESSAGE
    assert response.model == "topic-guard"
    assert agent.called is False