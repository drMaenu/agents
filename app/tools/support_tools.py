import re
from typing import Any

from app.data.error_codes import ERROR_CODE_DATABASE


def normalize_error_code(error_code: str) -> str:
    """
    Normalisiert einen Fehlercode für den Lookup.

    Beispiele:
    - "e-104" -> "E-104"
    - " e104 " -> "E104"
    - "4049" -> "4049"
    """
    return error_code.strip().upper()


def extract_error_code(text: str) -> str | None:
    """
    Extrahiert heuristisch einen Fehlercode aus einem Freitext.

    Unterstützte Beispiele:
    - E-104
    - e-104
    - F-2001
    - 4049
    """
    patterns = [
        r"\b[A-Za-z]-\d{2,6}\b",
        r"\b\d{3,6}\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return normalize_error_code(match.group(0))

    return None


def get_error_code_info(error_code: str) -> dict[str, Any] | None:
    """
    Liefert strukturierte Informationen zu einem Fehlercode aus der lokalen Datenbasis.
    """
    normalized_code = normalize_error_code(error_code)
    return ERROR_CODE_DATABASE.get(normalized_code)