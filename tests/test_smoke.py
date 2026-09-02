from app.models.chat_models import ChatRequest, ChatResponse
from app.services.chat_service import ChatService


class DummyAgent:
    def get_response(self, request: ChatRequest) -> ChatResponse:
        return ChatResponse(
            answer=f"Testantwort auf: {request.message}",
            model="dummy-model",
        )


def test_chat_service_returns_response() -> None:
    service = ChatService(agent=DummyAgent())
    request = ChatRequest(message="Hallo Support")

    response = service.process_chat(request)

    assert response.answer == "Testantwort auf: Hallo Support"
    assert response.model == "dummy-model"