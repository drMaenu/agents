from fastapi import FastAPI

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


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    """
    Einfache Root-Route.
    """
    return {"message": "Support Agent API is running"}