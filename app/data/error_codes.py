ERROR_CODE_DATABASE = {
    "E-104": {
        "title": "Kommunikationsfehler mit Sensorschnittstelle",
        "description": (
            "Das Gerät konnte keine stabile Verbindung zur internen oder externen "
            "Sensorschnittstelle aufbauen."
        ),
        "possible_causes": [
            "Locker sitzender oder beschädigter Sensorkabelanschluss",
            "Defekter Sensor",
            "Kurzzeitiger Kommunikationsabbruch nach Neustart",
            "Fehlerhafte Spannungsversorgung der Sensorschnittstelle",
        ],
        "recommended_actions": [
            "Gerät ausschalten und Spannungsversorgung prüfen",
            "Sensorverkabelung auf festen Sitz und sichtbare Schäden kontrollieren",
            "Gerät neu starten",
            "Falls möglich, Sensor testweise austauschen",
            "Wenn der Fehler bestehen bleibt, technischen Support kontaktieren",
        ],
        "severity": "medium",
    },
    "4049": {
        "title": "Ungültiger Parameterwert in Konfigurationsanfrage",
        "description": (
            "Ein übergebener Konfigurationswert konnte vom System nicht verarbeitet "
            "werden, weil er außerhalb des erlaubten Bereichs liegt oder ungültig formatiert ist."
        ),
        "possible_causes": [
            "Falscher Eingabewert in einer Konfigurationsmaske",
            "Nicht unterstützte Kombination von Parametern",
            "Veraltete Konfigurationsdaten",
            "Fehlerhafte Datenübergabe aus einer externen Schnittstelle",
        ],
        "recommended_actions": [
            "Eingegebene Konfigurationswerte prüfen",
            "Zuletzt geänderte Einstellungen zurücksetzen",
            "Format und Wertebereich der Eingaben kontrollieren",
            "Schnittstellen- oder Importdaten auf Konsistenz prüfen",
            "Bei wiederholtem Auftreten Support mit den konkreten Eingabewerten kontaktieren",
        ],
        "severity": "medium",
    },
    "F-2001": {
        "title": "Temperatursensor außerhalb Sollbereich",
        "description": (
            "Der gemessene Temperaturwert liegt außerhalb des zulässigen Betriebsbereichs "
            "oder der Sensor liefert unplausible Werte."
        ),
        "possible_causes": [
            "Defekter Temperatursensor",
            "Unterbrochene Sensorleitung",
            "Tatsächlich zu hohe oder zu niedrige Umgebungstemperatur",
            "Kalibrierungsproblem",
        ],
        "recommended_actions": [
            "Umgebungstemperatur prüfen",
            "Sensorleitung kontrollieren",
            "Gerät neu starten",
            "Sensorwerte im Diagnosemenü prüfen",
            "Bei anhaltendem Fehler Wartung veranlassen",
        ],
        "severity": "high",
    },
}