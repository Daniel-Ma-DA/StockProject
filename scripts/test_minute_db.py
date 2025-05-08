import duckdb
import os

# DB-Pfad
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
db_path = os.path.join(project_root, "db", "aktien.db")

# Verbindung herstellen
con = duckdb.connect(db_path)

# Test: Gibt es die Tabelle?
try:
    tables = con.execute("SHOW TABLES").fetchdf()
    print("📋 Tabellen in der DB:", tables)

    if "stockdata" not in tables["name"].values:
        print("❌ Tabelle 'stockdata' existiert NICHT.")
    else:
        # Vorschau auf Daten
        print("✅ Tabelle vorhanden – zeige erste 5 Zeilen:")
        df = con.execute("SELECT * FROM stockdata LIMIT 5").fetchdf()
        print(df)

        # Anzahl aller Zeilen
        count = con.execute("SELECT COUNT(*) FROM stockdata").fetchone()[0]
        print(f"📊 Anzahl Zeilen: {count}")

        # Optional: Anzahl einzigartiger Symbole
        symbol_count = con.execute("SELECT COUNT(DISTINCT symbol) FROM stockdata").fetchone()[0]
        print(f"🔣 Einzigartige Symbole: {symbol_count}")

except Exception as e:
    print("❌ Fehler beim Zugriff auf die Datenbank:", e)

con.close()
