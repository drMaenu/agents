from app.services.escalation_guard import evaluate_escalation


def test_escalates_on_direct_ticket_request():
    result = evaluate_escalation("Bitte Ticket erstellen.")

    assert result.escalate is True
    assert result.reason == "escalation_phrase_detected"


def test_escalates_on_failure_phrase():
    result = evaluate_escalation("Ich habe alles probiert, es geht immer noch nicht.")

    assert result.escalate is True
    assert result.reason == "escalation_phrase_detected"


def test_escalates_on_critical_outage_keyword():
    result = evaluate_escalation("Das Produktivsystem hat einen Totalausfall.")

    assert result.escalate is True
    assert result.reason == "escalation_keyword_detected"


def test_does_not_escalate_normal_support_request():
    result = evaluate_escalation("Mein WLAN funktioniert nicht.")

    assert result.escalate is False
    assert result.reason == "no_escalation_signal"