from app.services.topic_guard import evaluate_topic


def test_allows_message_with_error_code():
    result = evaluate_topic("Ich bekomme den Fehler E203 auf dem Gerät.")

    assert result.allowed is True
    assert result.reason == "error_code_detected"


def test_allows_message_with_support_keyword():
    result = evaluate_topic("Mein WLAN funktioniert nicht mehr.")

    assert result.allowed is True
    assert result.reason == "support_keyword_detected"


def test_rejects_off_topic_recipe_request():
    result = evaluate_topic("Gib mir ein Rezept für Lasagne.")

    assert result.allowed is False
    assert result.reason == "off_topic"


def test_rejects_general_knowledge_question():
    result = evaluate_topic("Wer war Albert Einstein?")

    assert result.allowed is False
    assert result.reason == "off_topic"


def test_rejects_empty_message():
    result = evaluate_topic("   ")

    assert result.allowed is False
    assert result.reason == "empty_message"