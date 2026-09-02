from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import setup_logging

settings = get_settings()
setup_logging(settings.log_level)

app = FastAPI(
    title="Support Agent API",
    version="0.1.0",
    description="First-Level-Support-System mit OpenAI-Anbindung",
)

app.include_router(router)

BASE_DIR = Path(__file__).resolve().parent
CHAT_UI_PATH = BASE_DIR / "web" / "static" / "chat.html"


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    """
    Einfache Root-Route.
    """
    return {"message": "Support Agent API is running"}


@app.get("/chat-ui", tags=["ui"])
def chat_ui() -> FileResponse:
    """
    Liefert eine einfache browserbasierte Chat-Oberfläche aus.
    """
    return FileResponse(CHAT_UI_PATH)