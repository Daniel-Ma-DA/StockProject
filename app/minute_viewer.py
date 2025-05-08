import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import os

# DB-Pfad
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
minute_db = os.path.join(project_root, "db", "aktien.db")
con = duckdb.connect(minute_db, read_only=True)

st.title("📈 Minutendaten-Viewer")

# Eingabefeld für Symbol
symbol = st.text_input("🔍 Symbol eingeben (z. B. AAPL)", "AAPL").strip().upper()

# Datumsbereich
col1, col2 = st.columns(2)
with col1:
    start = st.date_input("📅 Startdatum", pd.to_datetime("2022-01-01"))
with col2:
    end = st.date_input("📅 Enddatum", pd.to_datetime("2022-01-02"))

# Daten abrufen
if symbol:
    try:
        df = con.execute(f"""
            SELECT datetime, close
            FROM stockdata
            WHERE symbol = '{symbol}'
              AND CAST(datetime AS DATE) BETWEEN '{start}' AND '{end}'
            ORDER BY datetime
        """).fetchdf()

        if df.empty:
            st.warning("⚠️ Keine Daten für dieses Symbol oder Zeitraum.")
        else:
            st.subheader(f"📊 Verlauf für {symbol}")
            fig = px.line(df, x="datetime", y="close", title=f"{symbol} – Close Price")
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Fehler: {e}")
