import logging

from app.agents.support_agent import SupportAgent
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.topic_guard import (
    SUPPORT_REJECTION_MESSAGE,
    evaluate_topic_with_history,
)
from app.services.escalation_guard import ESCALATION_MESSAGE, evaluate_escalation

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

        guard_result = evaluate_topic_with_history(message, request.history)
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
        escalation_result = evaluate_escalation(message)
        logger.info(
            "Eskalations-Guard ausgewertet: escalate=%s, reason=%s",
            escalation_result.escalate,
            escalation_result.reason,
        )

        if escalation_result.escalate:
            return ChatResponse(
                answer=ESCALATION_MESSAGE,
                model="escalation-guard",
            )

        sanitized_request = ChatRequest(
            message=message,
            history=request.history,
        )
        return self.agent.get_response(sanitized_request)