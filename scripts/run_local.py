from app.core.config import get_settings
from app.core.logging import setup_logging
from app.models.chat_models import ChatRequest
from app.services.chat_service import ChatService


def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)

    service = ChatService()

    print("Lokaler Support-Chat gestartet. Beenden mit 'exit' oder 'quit'.")

    while True:
        user_input = input("\nDu: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Chat beendet.")
            break

        if not user_input:
            print("Bitte gib eine Nachricht ein.")
            continue

        try:
            request = ChatRequest(message=user_input)
            response = service.process_chat(request)
            print(f"\nAgent: {response.answer}")
        except Exception as exc:
            print(f"\nFehler: {exc}")


if __name__ == "__main__":
    main()