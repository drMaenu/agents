import logging

from app.agents.support_agent import SupportAgent
from app.models.chat_models import ChatRequest, ChatResponse

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
        """
        logger.info("Verarbeite Chat-Anfrage.")

        if not request.message.strip():
            raise ValueError("Die Nachricht darf nicht leer sein.")

        return self.agent.get_response(request)