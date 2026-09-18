from app.agents.support_agent import SupportAgent
from app.models.chat_models import ChatRequest
from app.models.chat_models import ChatMessage


def test_build_user_message_without_error_code() -> None:
    agent = SupportAgent()

    result = agent._build_user_message(
        ChatRequest(message="Mein Gerät funktioniert nicht richtig.")
    )

    assert "Aktuelle Nutzeranfrage:" in result
    assert "Mein Gerät funktioniert nicht richtig." in result
    assert "Zusätzlicher interner Support-Kontext:" not in result


def test_build_user_message_with_known_error_code() -> None:
    agent = SupportAgent()

    result = agent._build_user_message(
        ChatRequest(message="Mein Gerät zeigt E-104.")
    )

    assert "Aktuelle Nutzeranfrage:" in result
    assert "Mein Gerät zeigt E-104." in result
    assert "Zusätzlicher interner Support-Kontext:" in result
    assert '"detected_error_code": "E-104"' in result


def test_build_user_message_includes_history() -> None:
    agent = SupportAgent()

    result = agent._build_user_message(
        ChatRequest(
            message="Fehler 403 beim Login.",
            history=[
                ChatMessage(role="user", content="Ich kann mich nicht anmelden."),
                ChatMessage(role="assistant", content="Welche Fehlermeldung wird angezeigt?"),
            ],
        )
    )

    assert "Bisheriger Gesprächsverlauf:" in result
    assert "Benutzer: Ich kann mich nicht anmelden." in result
    assert "Agent: Welche Fehlermeldung wird angezeigt?" in result
    assert "Aktuelle Nutzeranfrage:" in result
    assert "Fehler 403 beim Login." in result