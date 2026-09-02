import logging

from openai import OpenAI

from app.core.config import get_settings
from app.models.chat_models import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)


class SupportAgent:
    """
    Einfacher Support-Agent mit echter OpenAI-Anbindung.

    Dieser Stand nutzt bewusst noch keinen komplexen Agenten-Workflow,
    sondern einen direkten Modellaufruf als stabile Grundlage.
    """

    def __init__(self) -> None:
        settings = get_settings()
        self.model = settings.openai_model
        self.client = OpenAI(api_key=settings.openai_api_key)

    def get_response(self, request: ChatRequest) -> ChatResponse:
        """
        Sendet die Benutzernachricht an das OpenAI-Modell und gibt die Antwort zurück.
        """
        logger.info("Sende Anfrage an OpenAI-Modell: %s", self.model)

        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "input_text",
                                "text": (
                                    "Du bist ein hilfreicher First-Level-Support-Agent. "
                                    "Antworte klar, freundlich und strukturiert. "
                                    "Wenn Informationen fehlen, weise knapp darauf hin. "
                                    "Erfinde keine internen Fakten."
                                ),
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": request.message,
                            }
                        ],
                    },
                ],
            )

            answer = response.output_text.strip()

            if not answer:
                logger.warning("OpenAI hat eine leere Antwort geliefert.")
                answer = "Ich konnte leider keine inhaltliche Antwort erzeugen."

            return ChatResponse(
                answer=answer,
                model=self.model,
            )

        except Exception as exc:
            logger.exception("Fehler bei der Kommunikation mit OpenAI.")
            raise RuntimeError("OpenAI-Anfrage fehlgeschlagen.") from exc