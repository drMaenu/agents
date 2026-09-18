from dataclasses import dataclass

ESCALATION_MESSAGE = (
    "Dieses Anliegen sollte an den nächsten Support-Level weitergegeben werden.\n\n"
    "Bitte halte für die Eskalation möglichst folgende Informationen bereit:\n"
    "1. betroffener Gerätetyp oder Produktname\n"
    "2. genaue Fehlermeldung oder Fehlercode\n"
    "3. bisher bereits getestete Schritte\n"
    "4. seit wann das Problem besteht\n"
    "5. Auswirkung des Problems auf den Betrieb"
)


@dataclass
class EscalationDecision:
    escalate: bool
    reason: str


ESCALATION_KEYWORDS = {
    "ticket",
    "eskalation",
    "eskalieren",
    "2nd level",
    "second level",
    "weitergeben",
    "weiterleiten",
    "serverfehler",
    "backendfehler",
    "hardwaredefekt",
    "totalausfall",
    "produktivsystem",
    "kritisch",
    "dringend",
    "nichts geht mehr",
    "komplett ausgefallen",
    "gerät defekt",
}

ESCALATION_PHRASES = {
    "bitte ticket erstellen",
    "an den second level",
    "an den 2nd level",
    "ich habe alles probiert",
    "es geht immer noch nicht",
    "bitte weitergeben",
    "bitte eskalieren",
    "system ist ausgefallen",
    "server ist nicht erreichbar",
}


def evaluate_escalation(message: str) -> EscalationDecision:
    normalized = message.strip().casefold()

    if not normalized:
        return EscalationDecision(escalate=False, reason="empty_message")

    if any(phrase in normalized for phrase in ESCALATION_PHRASES):
        return EscalationDecision(escalate=True, reason="escalation_phrase_detected")

    if any(keyword in normalized for keyword in ESCALATION_KEYWORDS):
        return EscalationDecision(escalate=True, reason="escalation_keyword_detected")

    return EscalationDecision(escalate=False, reason="no_escalation_signal")