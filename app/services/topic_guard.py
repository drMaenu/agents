from dataclasses import dataclass
import re

SUPPORT_REJECTION_MESSAGE = (
    "Ich unterstütze nur bei technischen Support-Anfragen zu Produkten, "
    "Fehlercodes, Bedienung, Konfiguration und Störungen. "
    "Wenn du ein konkretes Supportproblem hast, beschreibe bitte das Gerät, "
    "die Fehlermeldung oder den Fehlercode."
)

SUPPORT_KEYWORDS = {
    "fehler",
    "fehlercode",
    "störung",
    "stoerung",
    "problem",
    "gerät",
    "geraet",
    "konfiguration",
    "verbindung",
    "meldung",
    "support",
    "installation",
    "update",
    "login",
    "anmeldung",
    "wlan",
    "netzwerk",
    "drucker",
    "app",
    "software",
    "hardware",
    "einrichten",
    "konfigurieren",
    "passwort",
    "benutzer",
    "konto",
    "ticket",
    "zugang",
    "server",
    "client",
    "vpn",
}

SUPPORT_PHRASES = {
    "funktioniert nicht",
    "geht nicht",
    "kann mich nicht anmelden",
    "ich kann mich nicht anmelden",
    "wie richte ich",
    "wie konfiguriere ich",
    "warum funktioniert",
    "ich bekomme die meldung",
    "ich bekomme den fehler",
    "verbindung fehlgeschlagen",
    "kann nicht verbinden",
    "zeigt fehler",
    "zeigt einen fehler",
}

OFF_TOPIC_KEYWORDS = {
    "rezept",
    "kochen",
    "gedicht",
    "sommer",
    "wetter",
    "urlaub",
    "film",
    "kino",
    "song",
    "musik",
    "mathematik",
    "geschichte",
    "biografie",
    "einstein",
    "lasagne",
    "sport",
}

ERROR_CODE_PATTERN = re.compile(
    r"\b(?:[A-Z]{1,5}-?\d{2,5}|\d{3,5})\b",
    re.IGNORECASE,
)


@dataclass
class TopicGuardResult:
    allowed: bool
    reason: str


def normalize_message(message: str) -> str:
    return message.strip().casefold()


def contains_error_code(message: str) -> bool:
    return bool(ERROR_CODE_PATTERN.search(message))


def count_keyword_hits(message: str, keywords: set[str]) -> int:
    return sum(1 for keyword in keywords if keyword in message)


def evaluate_topic(message: str) -> TopicGuardResult:
    normalized = normalize_message(message)

    if not normalized:
        return TopicGuardResult(
            allowed=False,
            reason="empty_message",
        )

    if contains_error_code(message):
        return TopicGuardResult(
            allowed=True,
            reason="error_code_detected",
        )

    support_keyword_hits = count_keyword_hits(normalized, SUPPORT_KEYWORDS)
    support_phrase_hits = count_keyword_hits(normalized, SUPPORT_PHRASES)
    off_topic_hits = count_keyword_hits(normalized, OFF_TOPIC_KEYWORDS)

    score = support_keyword_hits + support_phrase_hits - (off_topic_hits * 2)

    if score >= 1:
        return TopicGuardResult(
            allowed=True,
            reason="support_score_detected",
        )

    return TopicGuardResult(
        allowed=False,
        reason="off_topic",
    )