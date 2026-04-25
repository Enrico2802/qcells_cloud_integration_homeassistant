# Qcells Cloud Home Assistant Integration

Dieses Repository enthält ein Home Assistant Custom-Integration-Scaffold für die Qcells Cloud.

## Inhalt
- `qcells_cloud/custom_components/qcells_cloud`: Custom Component für Home Assistant
- `requirements.txt`: Python-Abhängigkeiten, die für lokale Tests oder Entwicklung per `pip` installiert werden können

## Installation

### 1. Python-Abhängigkeiten installieren
Für lokale Entwicklung oder wenn du die Python-Bibliotheken manuell installieren möchtest:

```bash
python -m pip install -r requirements.txt
```

> Hinweis: `homeassistant` wird hier nicht als Pflicht-Installation aufgeführt. Wenn du die Integration in einer echten Home Assistant-Instanz nutzt, bringt Home Assistant selbst die benötigten Bibliotheken mit.

### 2. Home Assistant Custom Component installieren
1. Kopiere den Ordner `qcells_cloud/custom_components/qcells_cloud` nach `config/custom_components/qcells_cloud` in deiner Home Assistant-Installation.
2. Starte Home Assistant neu.
3. Gehe zu **Einstellungen → Geräte & Dienste → Integration hinzufügen**.
4. Suche nach **Qcells Cloud**.
5. Gib die folgenden Werte ein:
   - Base URL
   - WiFi SN
   - API key / tokenId
   - Abfrageintervall

## Hinweise
- Diese Integration ist für die Datenerfassung aus der Qcells Cloud gedacht.
- `requirements.txt` listet nur die Python-Pakete auf, die für Tests oder die Entwicklung benötigt werden.
- In Home Assistant werden die meisten Abhängigkeiten bereits durch die Plattform bereitgestellt.

## Unterstützte Module
- `aiohttp` für asynchrone HTTP-Abfragen
- `voluptuous` für die Eingabevalidierung im Config Flow
- `homeassistant` als Basisplattform

## Lizenz
Keine Lizenzinformation im Repository definiert. Füge bei Bedarf eine `LICENSE`-Datei hinzu.
