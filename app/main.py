import logging

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.models.chat_models import ChatRequest
from app.services.chat_service import ChatService


def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)

    logger = logging.getLogger(__name__)
    service = ChatService()

    request = ChatRequest(
        message="Hallo, mein Gerät zeigt den Fehler E-104. Was kann ich tun?"
    )

    try:
        response = service.process_chat(request)
        print("Antwort des Support-Agenten:")
        print(response.answer)
        print()
        print(f"Verwendetes Modell: {response.model}")
    except Exception as exc:
        logger.exception("Anwendungsausführung fehlgeschlagen.")
        print(f"Fehler: {exc}")


if __name__ == "__main__":
    main()