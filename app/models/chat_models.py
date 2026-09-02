from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Eingabemodell für eine Chat-Anfrage.
    """

    message: str = Field(..., min_length=1, description="Nachricht des Benutzers")


class ChatResponse(BaseModel):
    """
    Ausgabemodell für eine Chat-Antwort.
    """

    answer: str
    model: str