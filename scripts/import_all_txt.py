import os
import pandas as pd
import duckdb

# Pfad zum Projekt-Root ermitteln
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Pfade setzen relativ zum Projekt-Root
data_dir = os.path.join(project_root, "1MinuteStockData")
db_path = os.path.join(project_root, "db", "aktien.db")

# Ordner db erstellen, falls nicht vorhanden
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Verbindung zur DB
con = duckdb.connect(db_path)

# Spalten definieren
columns = ["date", "time", "open", "high", "low", "close", "volume"]

# Daten sammeln
all_data = []

for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        symbol = filename.replace(".txt", "")
        filepath = os.path.join(data_dir, filename)

        print(f"📥 Importiere {symbol}...")

        df = pd.read_csv(filepath, names=columns)
        df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])
        df.drop(["date", "time"], axis=1, inplace=True)
        df["symbol"] = symbol

        all_data.append(df)

# Alle Daten zusammenführen
df_all = pd.concat(all_data, ignore_index=True)

# Optional: Sortieren
df_all.sort_values(by=["symbol", "datetime"], inplace=True)

# Tabelle erstellen
con.execute("DROP TABLE IF EXISTS stockdata")
con.execute("CREATE TABLE stockdata AS SELECT * FROM df_all")

con.close()
print("✅ Import abgeschlossen – zentrale Tabelle 'stockdata' erstellt.")
