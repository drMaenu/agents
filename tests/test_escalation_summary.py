from app.models.chat_models import ChatMessage, ChatRequest
from app.services.escalation_summary import build_escalation_summary


def test_build_escalation_summary_without_history() -> None:
    request = ChatRequest(message="Bitte Ticket erstellen.")

    result = build_escalation_summary(
        request=request,
        escalation_reason="escalation_phrase_detected",
    )

    assert "Dieses Anliegen sollte an den nächsten Support-Level weitergegeben werden." in result
    assert "- Aktuelle Anfrage: Bitte Ticket erstellen." in result
    assert "- Erkannter Fehlercode: Kein Fehlercode erkannt" in result
    assert "- Kein bisheriger Verlauf vorhanden." in result
    assert "- Eskalationsgrund: escalation_phrase_detected" in result


def test_build_escalation_summary_with_history_and_error_code() -> None:
    request = ChatRequest(
        message="Es kommt Fehler 403 und nichts geht mehr.",
        history=[
            ChatMessage(role="user", content="Ich kann mich nicht anmelden."),
            ChatMessage(role="assistant", content="Tritt das Problem nur in der App auf?"),
            ChatMessage(role="user", content="Ja, nur in der App."),
        ],
    )

    result = build_escalation_summary(
        request=request,
        escalation_reason="escalation_keyword_detected",
    )

    assert "- Aktuelle Anfrage: Es kommt Fehler 403 und nichts geht mehr." in result
    assert "- Erkannter Fehlercode: 403" in result
    assert "  - Benutzer: Ich kann mich nicht anmelden." in result
    assert "  - Agent: Tritt das Problem nur in der App auf?" in result
    assert "  - Benutzer: Ja, nur in der App." in result
    assert "- Eskalationsgrund: escalation_keyword_detected" in result