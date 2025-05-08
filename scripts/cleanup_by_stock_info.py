import os
import pandas as pd

# Projektpfade
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_dir = os.path.join(project_root, "1MinuteStockData")
stock_info_path = os.path.join(project_root, "data", "StockInfo.txt")

# StockInfo einlesen
df_info = pd.read_csv(stock_info_path, sep="\t", comment="#", engine="python")
valid_symbols = set(df_info["Symbol"].dropna().astype(str).str.strip())

# Aufräumen starten
deleted = 0
kept = 0

for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        symbol = filename.replace(".txt", "").strip()
        if symbol not in valid_symbols:
            os.remove(os.path.join(data_dir, filename))
            deleted += 1
        else:
            kept += 1

print(f"✅ Aufräumen abgeschlossen: {kept} Aktien behalten, {deleted} gelöscht.")
