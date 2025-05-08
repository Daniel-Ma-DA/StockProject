import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import os

# DB-Pfad
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
daily_db = os.path.join(project_root, "db", "aktien_daily.db")
con = duckdb.connect(daily_db, read_only=True)

st.title("🚀 Top 3 Aktien – Performance seit Handelsstart")

# Alle Symbole + Performance berechnen
st.write("📊 Berechne Top Performer...")

query = """
WITH ranked AS (
    SELECT
        symbol,
        FIRST(close ORDER BY date) AS start_price,
        LAST(close ORDER BY date) AS end_price
    FROM stockdata_daily
    GROUP BY symbol
),
perf AS (
    SELECT
        symbol,
        ((end_price - start_price) / start_price) * 100 AS percent_gain
    FROM ranked
)
SELECT symbol FROM perf ORDER BY percent_gain DESC LIMIT 3;
"""

top3 = con.execute(query).fetchdf()["symbol"].tolist()

st.success(f"🏆 Top 3 Symbole: {', '.join(top3)}")

# Kursverläufe holen
df = con.execute(f"""
    SELECT symbol, date, close
    FROM stockdata_daily
    WHERE symbol IN {tuple(top3)}
    ORDER BY date
""").fetchdf()

# Normalisieren der Kurse
df["close_norm"] = df.groupby("symbol")["close"].transform(lambda x: x / x.iloc[0] * 100)

# Plot
fig = px.line(df, x="date", y="close_norm", color="symbol",
              title="📈 Kursverlauf (normalisiert auf 100%) – Top 3 Performer",
              labels={"close_norm": "Normierter Kurs (%)", "date": "Datum"})

st.plotly_chart(fig, use_container_width=True)
