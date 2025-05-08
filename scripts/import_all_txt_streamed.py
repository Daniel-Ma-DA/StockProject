import os
import pandas as pd
import duckdb

# Pfade
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_dir = os.path.join(project_root, "1MinuteStockData")
db_path = os.path.join(project_root, "db", "aktien.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Verbindung
con = duckdb.connect(db_path)

# Tabelle anlegen, wenn sie nicht existiert
con.execute("""
    CREATE TABLE IF NOT EXISTS stockdata (
        datetime TIMESTAMP,
        open DOUBLE,
        high DOUBLE,
        low DOUBLE,
        close DOUBLE,
        volume BIGINT,
        symbol TEXT
    )
""")

# Spalten
columns = ["date", "time", "open", "high", "low", "close", "volume"]

# Vorhandene Symbole aus DB holen
existing_symbols = set(
    con.execute("SELECT DISTINCT symbol FROM stockdata").fetchdf()["symbol"]
)

for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        symbol = filename.replace(".txt", "").strip()

        if symbol in existing_symbols:
            print(f"⏭️  Überspringe {symbol} – schon vorhanden.")
            continue

        filepath = os.path.join(data_dir, filename)
        print(f"📥 Importiere {symbol}...")

        try:
            df = pd.read_csv(filepath, names=columns, low_memory=False)
            df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], errors="coerce")
            df.drop(columns=["date", "time"], inplace=True)
            df["symbol"] = symbol
            df.dropna(subset=["datetime"], inplace=True)

            con.register("temp_df", df)
            con.execute("""
                INSERT INTO stockdata
                SELECT datetime, open, high, low, close, volume, symbol FROM temp_df
            """)
            con.unregister("temp_df")

        except Exception as e:
            print(f"❌ Fehler bei {symbol}: {e}")

con.close()
print("✅ Import abgeschlossen.")
