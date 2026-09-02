from app.agents.support_agent import SupportAgent


def test_build_user_message_without_error_code() -> None:
    agent = SupportAgent()
    result = agent._build_user_message("Mein Gerät funktioniert nicht richtig.")

    assert "Zusätzlicher interner Support-Kontext" not in result
    assert result == "Mein Gerät funktioniert nicht richtig."


def test_build_user_message_with_known_error_code() -> None:
    agent = SupportAgent()
    result = agent._build_user_message("Mein Gerät zeigt E-104.")

    assert "Zusätzlicher interner Support-Kontext" in result
    assert "E-104" in result
    assert "Kommunikationsfehler mit Sensorschnittstelle" in result