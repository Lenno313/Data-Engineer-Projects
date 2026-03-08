import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
import pandas as pd
from streamlit_autorefresh import st_autorefresh # <-- Importieren

st_autorefresh(interval=30000, key="datarefresh")

host = os.getenv("DB_HOST", "localhost") 
user = os.getenv("DB_USER")
pw = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT", "5432")
engine = create_engine(f"postgresql://{user}:{pw}@{host}:{port}/fut_database")

st.set_page_config(page_title="FUT Hub", layout="wide")

@st.cache_data(ttl=60)
def get_system_stats():
    c_players = pd.read_sql("SELECT COUNT(*) FROM players", engine).iloc[0, 0] # Spieleranzahl
    c_prices = pd.read_sql("SELECT COUNT(*) FROM prices", engine).iloc[0, 0] # Preisanzahl
    c_snaps = pd.read_sql("SELECT COUNT(*) FROM rating_snapshots", engine).iloc[0, 0] # Rating snapshots
    l_update = pd.read_sql("SELECT MAX(timestamp) FROM prices", engine).iloc[0, 0] # letztes update
    return c_players, c_prices, c_snaps, l_update

st.title("FUT Market Dashboard")

try:
    c_players, c_prices, c_snaps, l_update = get_system_stats()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Getrackte Spieler", f"{c_players}")
    col2.metric("Preis-Datenpunkte", f"{c_prices:,}".replace(",", "."))
    col3.metric("Markt-Snapshots", f"{c_snaps}")

    st.sidebar.success("Pipeline läuft auf Pi.")
    st.sidebar.caption(f"Letzter Sync: {l_update} (UTC)")
    
except Exception as e:
    st.error(f"Datenbankverbindung fehlgeschlagen: {e}")