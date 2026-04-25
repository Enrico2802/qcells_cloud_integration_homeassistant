# Qcells Cloud Home Assistant Integration

Dieses Repository enthält ein Home Assistant Custom-Integration-Scaffold für die Qcells Cloud.

## Inhalt
- `qcells_cloud/custom_components/qcells_cloud`: Custom Component für Home Assistant
- `qcells_cloud/custom_components/qcells_cloud/test_api.py`: Standalone Python-Skript zum Testen der Qcells API
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
   - LAN Adapter Registration number (NICHT die Wechselrichter Device SN!)
   - API key / tokenId
   - Abfrageintervall

## API testen

Um die Qcells API unabhängig von Home Assistant zu testen:

1. **Umgebung einrichten:**
   ```bash
   # Kopiere die Beispiel-Konfigurationsdatei
   cp .env.example .env

   # Bearbeite .env und setze deine echten Werte
   nano .env  # oder verwende deinen bevorzugten Editor
   ```

2. **Python-Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test-Skript ausführen:**
   ```bash
   cd qcells_cloud/custom_components/qcells_cloud
   python test_api.py
   ```

### 🔒 Sicherheitshinweis

Die `.env` Datei enthält sensible Daten und wird von Git ignoriert (siehe `.gitignore`). Stelle sicher, dass du die `.env` Datei niemals in Git committest!

## 🐙 GitHub-Veröffentlichung

Um dieses Projekt sicher auf GitHub zu veröffentlichen:

1. **Vor dem ersten Commit:**
   ```bash
   # Erstelle deine .env Datei (wird ignoriert)
   cp .env.example .env
   # Bearbeite .env mit deinen echten Werten
   ```

2. **Überprüfe, was committet wird:**
   ```bash
   git status
   git add .
   git status  # Stelle sicher, dass .env NICHT in der Liste ist
   ```

3. **Commit und Push:**
   ```bash
   git commit -m "Initial commit: Qcells Cloud Home Assistant Integration"
   git push origin main
   ```

Die `.gitignore` Datei stellt sicher, dass sensible Daten nicht veröffentlicht werden.

## Unterstützte Module
- `aiohttp` für asynchrone HTTP-Abfragen
- `voluptuous` für die Eingabevalidierung im Config Flow
- `homeassistant` als Basisplattform

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

