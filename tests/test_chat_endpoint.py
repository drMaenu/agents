from fastapi.testclient import TestClient

from app.api import routes
from app.main import app
from app.models.chat_models import ChatResponse

client = TestClient(app)


class DummyChatService:
    def process_chat(self, request):
        return ChatResponse(
            answer=f"Dummy-Antwort: {request.message}",
            model="dummy-model",
        )


def test_chat_endpoint_returns_response() -> None:
    original_service = routes.chat_service
    routes.chat_service = DummyChatService()

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
    finally:
        routes.chat_service = original_service