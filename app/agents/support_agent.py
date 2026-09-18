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

    def _format_history(self, history: list[ChatMessage]) -> str:
        """
        Formatiert den bisherigen Chatverlauf als Textblock.
        """
        if not history:
            return ""

        lines = []
        for item in history:
            if item.role == "user":
                prefix = "Benutzer"
            elif item.role == "assistant":
                prefix = "Agent"
            else:
                logger.warning("Unbekannte History-Rolle übersprungen: %s", item.role)
                continue

            lines.append(f"{prefix}: {item.content}")

        if not lines:
            return ""

        return "Bisheriger Gesprächsverlauf:\n" + "\n".join(lines)

    def _build_user_message(self, request: ChatRequest) -> str:
        """
        Baut die Nutzernachricht optional mit Verlauf und ergänztem Tool-Kontext auf.
        """
        parts = []

        history_text = self._format_history(request.history)
        if history_text:
            parts.append(history_text)

        parts.append(f"Aktuelle Nutzeranfrage:\n{request.message}")

        error_code = extract_error_code(request.message)

        if error_code:
            error_info = get_error_code_info(error_code)

            if error_info:
                logger.info("Lokaler Wissenseintrag für Fehlercode gefunden: %s", error_code)

                tool_context = {
                    "detected_error_code": error_code,
                    "error_code_details": error_info,
                }

                parts.append(
                    "Zusätzlicher interner Support-Kontext:\n"
                    f"{json.dumps(tool_context, ensure_ascii=False, indent=2)}"
                )
            else:
                logger.info("Kein lokaler Wissenseintrag für Fehlercode gefunden: %s", error_code)

        parts.append("Nutze diese Informationen für eine präzise Support-Antwort.")

        return "\n\n".join(parts)

    def get_response(self, request: ChatRequest) -> ChatResponse:
        """
        Sendet die Benutzernachricht an das OpenAI-Modell und gibt die Antwort zurück.
        """
        logger.info("Sende Anfrage an OpenAI-Modell: %s", self.model)

        system_prompt = self._build_system_prompt()
        user_message = self._build_user_message(request)

        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "input_text",
                                "text": system_prompt,
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": user_message,
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