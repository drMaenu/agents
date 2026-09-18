from app.services.topic_guard import evaluate_topic
from app.models.chat_models import ChatMessage
from app.services.topic_guard import evaluate_topic_with_history


def test_allows_message_with_error_code():
    result = evaluate_topic("Ich bekomme den Fehler E203 auf dem Gerät.")

    assert result.allowed is True
    assert result.reason == "error_code_detected"


def test_allows_message_with_support_keyword():
    result = evaluate_topic("Mein WLAN funktioniert nicht mehr.")

    assert result.allowed is True
    assert result.reason == "support_score_detected"


def test_allows_message_with_support_phrase():
    result = evaluate_topic("Ich kann mich nicht anmelden.")

    assert result.allowed is True
    assert result.reason == "support_score_detected"


def test_allows_device_configuration_question():
    result = evaluate_topic("Wie konfiguriere ich das Gerät?")

    assert result.allowed is True
    assert result.reason == "support_score_detected"


def test_rejects_off_topic_recipe_request():
    result = evaluate_topic("Gib mir ein Rezept für Lasagne.")

    assert result.allowed is False
    assert result.reason == "off_topic"


def test_rejects_general_knowledge_question():
    result = evaluate_topic("Wer war Albert Einstein?")

    assert result.allowed is False
    assert result.reason == "off_topic"


def test_rejects_poem_request():
    result = evaluate_topic("Schreibe mir ein Gedicht über den Sommer.")

    assert result.allowed is False
    assert result.reason == "off_topic"


def test_rejects_empty_message():
    result = evaluate_topic("   ")

    assert result.allowed is False
    assert result.reason == "empty_message"


def test_allows_mixed_support_request_with_app_error():
    result = evaluate_topic("Die App zeigt Fehler 403 beim Login.")

    assert result.allowed is True
    assert result.reason == "error_code_detected"


def test_rejects_non_support_learning_request():
    result = evaluate_topic("Kannst du mir bei Mathematik helfen?")

    assert result.allowed is False
    assert result.reason == "off_topic"


def test_allows_numeric_error_code():
    result = evaluate_topic("Ich bekomme den Fehler 1001 beim Start der App.")

    assert result.allowed is True
    assert result.reason == "error_code_detected"


def test_does_not_treat_small_number_alone_as_error_code():
    result = evaluate_topic("Ich habe 2 Fragen.")

    assert result.allowed is False
    assert result.reason == "off_topic"


def test_does_not_treat_version_number_alone_as_support_request():
    result = evaluate_topic("Version 11 ist heute erschienen.")

    assert result.allowed is False
    assert result.reason == "off_topic"


def test_allows_short_follow_up_with_support_context():
    result = evaluate_topic_with_history(
        "HP LaserJet",
        history=[
            ChatMessage(role="user", content="Mein Drucker funktioniert nicht."),
            ChatMessage(role="assistant", content="Welches Modell ist es?"),
        ],
    )

    assert result.allowed is True
    assert result.reason == "follow_up_with_support_context"


def test_allows_yes_as_follow_up_with_support_context():
    result = evaluate_topic_with_history(
        "Ja",
        history=[
            ChatMessage(role="user", content="Ich kann mich nicht anmelden."),
            ChatMessage(role="assistant", content="Tritt das Problem nur in der App auf?"),
        ],
    )

    assert result.allowed is True
    assert result.reason == "follow_up_with_support_context"


def test_rejects_short_follow_up_without_support_context():
    result = evaluate_topic_with_history(
        "Ja",
        history=[
            ChatMessage(role="user", content="Erzähl mir etwas über Musik."),
            ChatMessage(role="assistant", content="Welches Genre interessiert dich?"),
        ],
    )

    assert result.allowed is False


def test_allows_ticket_request_as_support_topic():
    result = evaluate_topic("Bitte Ticket erstellen.")

    assert result.allowed is True


def test_allows_escalation_phrase_as_support_topic():
    result = evaluate_topic("Ich habe alles probiert, es geht immer noch nicht.")

    assert result.allowed is True


def test_allows_critical_outage_as_support_topic():
    result = evaluate_topic("Das Produktivsystem hat einen Totalausfall.")

    assert result.allowed is True