from app.tools.support_tools import (
    extract_error_code,
    get_error_code_info,
    normalize_error_code,
)


def test_normalize_error_code_keeps_numeric_code() -> None:
    assert normalize_error_code("4049") == "4049"


def test_normalize_error_code_uppercases_alphanumeric_code() -> None:
    assert normalize_error_code("e-104") == "E-104"


def test_extract_error_code_finds_alphanumeric_code() -> None:
    text = "Mein Gerät zeigt den Fehler E-104 beim Start."
    assert extract_error_code(text) == "E-104"


def test_extract_error_code_finds_numeric_code() -> None:
    text = "Ich bekomme immer den Fehlercode 4049."
    assert extract_error_code(text) == "4049"


def test_extract_error_code_returns_none_if_not_found() -> None:
    text = "Das Gerät verhält sich komisch, aber ohne Code."
    assert extract_error_code(text) is None


def test_get_error_code_info_returns_data_for_known_code() -> None:
    result = get_error_code_info("E-104")

    assert result is not None
    assert result["title"] == "Kommunikationsfehler mit Sensorschnittstelle"


def test_get_error_code_info_returns_none_for_unknown_code() -> None:
    assert get_error_code_info("E-999") is None