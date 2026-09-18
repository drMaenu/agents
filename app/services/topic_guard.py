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
    "melding",
    "meldung",
    "support",
    "installation",
    "update",
    "login",
    "anmeldung",
    "funktioniert nicht",
    "geht nicht",
    "wlan",
    "netzwerk",
    "app",
    "software",
    "hardware",
    "einrichten",
    "konfigurieren",
    "benutzer",
    "konto",
}

ERROR_CODE_PATTERN = re.compile(r"\b[A-Z]{1,3}-?\d{2,5}\b", re.IGNORECASE)


@dataclass
class TopicGuardResult:
    allowed: bool
    reason: str


def contains_support_keyword(message: str) -> bool:
    normalized = message.casefold()
    return any(keyword in normalized for keyword in SUPPORT_KEYWORDS)


def contains_error_code(message: str) -> bool:
    return bool(ERROR_CODE_PATTERN.search(message))


def evaluate_topic(message: str) -> TopicGuardResult:
    normalized = message.strip()

    if not normalized:
        return TopicGuardResult(
            allowed=False,
            reason="empty_message",
        )

    if contains_error_code(normalized):
        return TopicGuardResult(
            allowed=True,
            reason="error_code_detected",
        )

    if contains_support_keyword(normalized):
        return TopicGuardResult(
            allowed=True,
            reason="support_keyword_detected",
        )

    return TopicGuardResult(
        allowed=False,
        reason="off_topic",
    )