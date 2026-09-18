from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., description="Rolle der Nachricht, z. B. user oder assistant")
    content: str = Field(..., min_length=1, description="Inhalt der Nachricht")


class ChatRequest(BaseModel):
    """
    Eingabemodell für eine Chat-Anfrage.
    """

    message: str = Field(..., min_length=1, description="Nachricht des Benutzers")
    history: list[ChatMessage] = Field(default_factory=list, description="Bisheriger Chatverlauf")


class ChatResponse(BaseModel):
    """
    Ausgabemodell für eine Chat-Antwort.
    """

    answer: str
    model: str