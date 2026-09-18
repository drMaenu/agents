from fastapi.testclient import TestClient

from app.api import routes
from app.main import app
from app.models.chat_models import ChatResponse
from app.services.chat_service import ChatService
from app.services.topic_guard import SUPPORT_REJECTION_MESSAGE

client = TestClient(app)


class DummyChatService:
    def __init__(self) -> None:
        self.called = False

    def process_chat(self, request):
        self.called = True
        return ChatResponse(
            answer=f"Dummy-Antwort: {request.message}",
            model="dummy-model",
        )


class DummyAgent:
    def __init__(self) -> None:
        self.called = False

    def get_response(self, request):
        self.called = True
        return ChatResponse(
            answer=f"Agent-Antwort: {request.message}",
            model="dummy-agent",
        )


def test_chat_endpoint_returns_response() -> None:
    original_service = routes.chat_service
    dummy_service = DummyChatService()
    routes.chat_service = dummy_service

    try:
        response = client.post(
            "/chat",
            json={"message": "Hallo API"},
        )

        assert response.status_code == 200
        assert response.json() == {
            "answer": "Dummy-Antwort: Hallo API",
            "model": "dummy-model",
        }
        assert dummy_service.called is True
    finally:
        routes.chat_service = original_service


def test_chat_endpoint_rejects_off_topic_request() -> None:
    original_service = routes.chat_service
    dummy_agent = DummyAgent()
    routes.chat_service = ChatService(agent=dummy_agent)

    try:
        response = client.post(
            "/chat",
            json={"message": "Schreibe mir ein Gedicht über den Sommer."},
        )

        assert response.status_code == 200
        assert response.json() == {
            "answer": SUPPORT_REJECTION_MESSAGE,
            "model": "topic-guard",
        }
        assert dummy_agent.called is False
    finally:
        routes.chat_service = original_service


def test_chat_endpoint_accepts_history() -> None:
    original_service = routes.chat_service
    routes.chat_service = DummyChatService()

    try:
        response = client.post(
            "/chat",
            json={
                "message": "Fehler 403 beim Login.",
                "history": [
                    {"role": "user", "content": "Ich kann mich nicht anmelden."},
                    {"role": "assistant", "content": "Welche Fehlermeldung wird angezeigt?"},
                ],
            },
        )

        assert response.status_code == 200
        assert response.json() == {
            "answer": "Dummy-Antwort: Fehler 403 beim Login.",
            "model": "dummy-model",
        }
    finally:
        routes.chat_service = original_service