import os
import pandas as pd
import duckdb

# Projektstruktur
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_dir = os.path.join(project_root, "kibotdownloadDayETFAndStock")
db_path = os.path.join(project_root, "db", "aktien_daily.db")
stock_info_path = os.path.join(project_root, "Data", "StockInfo.txt")

# Whitelist laden
df_info = pd.read_csv(stock_info_path, sep="\t", comment="#", engine="python")
df_info.columns = df_info.columns.str.strip()
valid_symbols = set(df_info["Symbol"].dropna().astype(str).str.strip())

# Verbindung zu neuer Datenbank
os.makedirs(os.path.dirname(db_path), exist_ok=True)
con = duckdb.connect(db_path)

# Tabelle erstellen, wenn nicht vorhanden
con.execute("""
    CREATE TABLE IF NOT EXISTS stockdata_daily (
        date DATE,
        open DOUBLE,
        high DOUBLE,
        low DOUBLE,
        close DOUBLE,
        volume BIGINT,
        symbol TEXT
    )
""")

# Vorhandene Symbole prüfen
existing_symbols = set(
    con.execute("SELECT DISTINCT symbol FROM stockdata_daily").fetchdf()["symbol"]
)

# Spaltenformat der Tagesdaten
columns = ["date", "open", "high", "low", "close", "volume"]

for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        symbol = filename.replace(".txt", "").strip()

        if symbol not in valid_symbols:
            print(f"⏭️  {symbol} ist kein gültiges Symbol – übersprungen.")
            continue

        if symbol in existing_symbols:
            print(f"⏭️  {symbol} bereits importiert – übersprungen.")
            continue

        filepath = os.path.join(data_dir, filename)
        print(f"📥 Importiere {symbol}...")

        try:
            df = pd.read_csv(filepath, names=columns, low_memory=False)
            df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
            df["symbol"] = symbol
            df.dropna(subset=["date"], inplace=True)

            con.register("temp_df", df)
            con.execute("""
                INSERT INTO stockdata_daily
                SELECT date, open, high, low, close, volume, symbol FROM temp_df
            """)
            con.unregister("temp_df")

        except Exception as e:
            print(f"❌ Fehler bei {symbol}: {e}")

con.close()
print("✅ Tagesdaten-Import abgeschlossen.")
