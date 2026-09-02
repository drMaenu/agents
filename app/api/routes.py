import logging

from fastapi import APIRouter, HTTPException, status

from app.models.chat_models import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter()
chat_service = ChatService()


@router.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """
    Einfache Health-Prüfung für lokale Tests und spätere Container-/Load-Balancer-Checks.
    """
    return {"status": "ok"}


@router.post(
    "/chat",
    response_model=ChatResponse,
    tags=["chat"],
    status_code=status.HTTP_200_OK,
)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Verarbeitet eine Chat-Anfrage über den Support-Agenten.
    """
    try:
        logger.info("HTTP /chat Anfrage empfangen.")
        return chat_service.process_chat(request)
    except ValueError as exc:
        logger.warning("Ungültige Chat-Anfrage: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        logger.exception("Fehler bei der Verarbeitung der Chat-Anfrage.")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Fehler bei der Kommunikation mit dem KI-Dienst.",
        ) from exc
    except Exception as exc:
        logger.exception("Unerwarteter Fehler im /chat Endpoint.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Interner Serverfehler.",
        ) from exc