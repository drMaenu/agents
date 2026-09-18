import json
import logging

from openai import OpenAI

from app.core.config import get_settings
from app.models.chat_models import ChatMessage, ChatRequest, ChatResponse
from app.tools.support_tools import extract_error_code, get_error_code_info

logger = logging.getLogger(__name__)


class SupportAgent:
    """
    Support-Agent mit OpenAI-Anbindung und einfachem Fehlercode-Lookup.
    """

    def __init__(self) -> None:
        settings = get_settings()
        self.model = settings.openai_model
        self.client = OpenAI(api_key=settings.openai_api_key)

    def _build_system_prompt(self) -> str:
        """
        Erzeugt den System-Prompt für den Support-Agenten.
        """
        return (
            "Du bist ein hilfreicher First-Level-Support-Agent. "
            "Antworte klar, freundlich und strukturiert. "
            "Nutze bereitgestellte technische Informationen vorrangig. "
            "Erfinde keine Produktdetails oder internen Fakten. "
            "Wenn ein Fehlercode bekannt ist, erkläre Bedeutung, mögliche Ursachen "
            "und sinnvolle nächste Schritte. "
            "Wenn Informationen fehlen, frage gezielt und knapp nach."
        )

    def _build_user_message(self, user_text: str) -> str:
        """
        Baut die Nutzernachricht optional mit ergänztem Tool-Kontext auf.
        """
        error_code = extract_error_code(user_text)

        if not error_code:
            return user_text

        error_info = get_error_code_info(error_code)

        if not error_info:
            logger.info("Kein lokaler Wissenseintrag für Fehlercode gefunden: %s", error_code)
            return user_text

        logger.info("Lokaler Wissenseintrag für Fehlercode gefunden: %s", error_code)

        tool_context = {
            "detected_error_code": error_code,
            "error_code_details": error_info,
        }

        return (
            f"Nutzeranfrage:\n{user_text}\n\n"
            "Zusätzlicher interner Support-Kontext:\n"
            f"{json.dumps(tool_context, ensure_ascii=False, indent=2)}\n\n"
            "Nutze diese Informationen für eine präzise Support-Antwort."
        )

    def _build_history_messages(self, history: list[ChatMessage]) -> list[dict]:
        """
        Konvertiert den Chatverlauf in das erwartete OpenAI-Input-Format.
        Nur user- und assistant-Nachrichten werden übernommen.
        """
        messages = []

        for item in history:
            if item.role not in {"user", "assistant"}:
                logger.warning("Unbekannte History-Rolle übersprungen: %s", item.role)
                continue

            messages.append(
                {
                    "role": item.role,
                    "content": [
                        {
                            "type": "input_text",
                            "text": item.content,
                        }
                    ],
                }
            )

        return messages

    def _build_model_input(self, request: ChatRequest) -> list[dict]:
        """
        Baut den vollständigen Input für das OpenAI-Modell:
        System-Prompt, Chat-Historie und aktuelle Benutzernachricht.
        """
        system_prompt = self._build_system_prompt()
        user_message = self._build_user_message(request.message)

        model_input = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": system_prompt,
                    }
                ],
            }
        ]

        model_input.extend(self._build_history_messages(request.history))
        model_input.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": user_message,
                    }
                ],
            }
        )

        return model_input

    def get_response(self, request: ChatRequest) -> ChatResponse:
        """
        Sendet die Benutzernachricht an das OpenAI-Modell und gibt die Antwort zurück.
        """
        logger.info("Sende Anfrage an OpenAI-Modell: %s", self.model)

        try:
            response = self.client.responses.create(
                model=self.model,
                input=self._build_model_input(request),
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