import duckdb
import os

# DB-Pfad
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
db_path = os.path.join(project_root, "db", "aktien_daily.db")

# Verbindung herstellen
con = duckdb.connect(db_path)

# Test: Gibt es die Tabelle?
try:
    tables = con.execute("SHOW TABLES").fetchdf()
    print("📋 Tabellen in der DB:", tables)

    if "stockdata_daily" not in tables["name"].values:
        print("❌ Tabelle 'stockdata_daily' existiert NICHT.")
    else:
        # Vorschau auf Daten
        print("✅ Tabelle vorhanden – zeige erste 5 Zeilen:")
        df = con.execute("SELECT * FROM stockdata_daily WHERE symbol = 'CELC'").fetchdf()

        print(df)

        # Anzahl aller Zeilen
        count = con.execute("SELECT COUNT(*) FROM stockdata_daily").fetchone()[0]
        print(f"📊 Anzahl Zeilen: {count}")

except Exception as e:
    print("❌ Fehler beim Zugriff auf die Datenbank:", e)

con.close()