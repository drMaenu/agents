import logging

from app.agents.support_agent import SupportAgent
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.topic_guard import evaluate_topic, SUPPORT_REJECTION_MESSAGE

logger = logging.getLogger(__name__)


class ChatService:
    """
    Service-Schicht für Chat-Anfragen.
    """

    def __init__(self, agent: SupportAgent | None = None) -> None:
        self.agent = agent or SupportAgent()

    def process_chat(self, request: ChatRequest) -> ChatResponse:
        """
        Validiert und verarbeitet eine Chat-Anfrage über den Support-Agenten.
        Bei Off-Topic-Anfragen wird keine Modellanfrage ausgeführt.
        """
        logger.info("Verarbeite Chat-Anfrage.")

        message = request.message.strip()
        if not message:
            raise ValueError("Die Nachricht darf nicht leer sein.")

        guard_result = evaluate_topic(message)
        logger.info(
            "Topic-Guard ausgewertet: allowed=%s, reason=%s",
            guard_result.allowed,
            guard_result.reason,
        )

        if not guard_result.allowed:
            return ChatResponse(
                answer=SUPPORT_REJECTION_MESSAGE,
                model="topic-guard",
            )

        sanitized_request = ChatRequest(
            message=message,
            history=request.history,
        )
        return self.agent.get_response(sanitized_request)