# Datenanalyse-Projekt

## Projektbeschreibung
Dieses Projekt lädt Daten von einer Website herunter, speichert sie in einer SQLite-Datenbank und analysiert sie. Es dient zur Hypothesentestung basierend auf den heruntergeladenen Daten.

## Verzeichnisstruktur
```
/mein-projekt
│-- /data                # Ordner für gespeicherte Daten
│-- /src                 # Quellcode
│   ├── fetch_data.py    # Script zum Herunterladen der Daten
│   ├── analyze_data.py  # Script zur Analyse und Hypothesentests
│   ├── database.py      # Script zur Verwaltung der SQLite-Datenbank
│-- requirements.txt     # Abhängigkeiten
│-- README.md            # Dokumentation
```

## Installation & Setup
1. **Python installieren** (falls nicht vorhanden): [Python Download](https://www.python.org/downloads/)
2. **Projektverzeichnis klonen oder erstellen**:
   ```sh
   git clone <repository-url>
   cd mein-projekt
   ```
3. **Virtuelle Umgebung erstellen (empfohlen)**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
4. **Abhängigkeiten installieren**:
   ```sh
   pip install -r requirements.txt
   ```

## Daten abrufen und speichern
Zum Herunterladen und Speichern der Daten in die SQLite-Datenbank:
```sh
python src/fetch_data.py
```

## Datenbank initialisieren
Falls die Datenbank noch nicht existiert, erstelle sie mit:
```sh
python src/database.py
```

## Daten analysieren
Zum Analysieren der gespeicherten Daten:
```sh
python src/analyze_data.py
```

## Anpassung der Datenquelle
Falls eine andere API oder Quelle genutzt werden soll, die URL in `fetch_data.py` ändern:
```python
URL = "https://api.example.com/data"
```

## Anforderungen
- Python 3.8+
- `requests`-Bibliothek (wird durch `requirements.txt` installiert)
- `sqlite3` (in Python enthalten)

## Erweiterungsideen
- Komplexere Analysen mit `pandas`
- Datenvisualisierung mit `matplotlib`
- Erweiterung auf eine relationale Datenbank wie PostgreSQL oder MySQL
- Automatische Updates mit `cron` oder `Windows Task Scheduler`

