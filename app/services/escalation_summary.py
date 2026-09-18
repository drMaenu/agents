from app.models.chat_models import ChatMessage, ChatRequest
from app.tools.support_tools import extract_error_code


def _format_history(history: list[ChatMessage]) -> str:
    """
    Formatiert den bisherigen Chatverlauf für die Eskalationszusammenfassung.
    """
    if not history:
        return "- Kein bisheriger Verlauf vorhanden."

    lines = []
    for item in history:
        if item.role == "user":
            prefix = "Benutzer"
        elif item.role == "assistant":
            prefix = "Agent"
        else:
            prefix = item.role

        lines.append(f"  - {prefix}: {item.content}")

    return "\n".join(lines)


def build_escalation_summary(request: ChatRequest, escalation_reason: str) -> str:
    """
    Erzeugt eine strukturierte Eskalationszusammenfassung aus aktueller Anfrage und Verlauf.
    """
    error_code = extract_error_code(request.message)

    summary_lines = [
        "Dieses Anliegen sollte an den nächsten Support-Level weitergegeben werden.",
        "",
        "Eskalationszusammenfassung:",
        f"- Aktuelle Anfrage: {request.message}",
        f"- Erkannter Fehlercode: {error_code if error_code else 'Kein Fehlercode erkannt'}",
        "- Bisheriger Verlauf:",
        _format_history(request.history),
        f"- Eskalationsgrund: {escalation_reason}",
        "",
        "Bitte halte für die Eskalation möglichst folgende Informationen bereit:",
        "1. betroffener Gerätetyp oder Produktname",
        "2. genaue Fehlermeldung oder Fehlercode",
        "3. bisher bereits getestete Schritte",
        "4. seit wann das Problem besteht",
        "5. Auswirkung des Problems auf den Betrieb",
    ]

    return "\n".join(summary_lines)