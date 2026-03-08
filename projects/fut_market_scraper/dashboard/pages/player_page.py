import streamlit as st
import pandas as pd
import plotly.express as px
from fut_dashboard import engine

st.title("Entwicklung der Spielerpreise")

# 1. Spieler wählen (Name aus players Tabelle)
query_players = "SELECT futwiz_id, first_name || ' ' || last_name as full_name FROM players"
df_players = pd.read_sql(query_players, engine)
selected_player_id = st.selectbox("Spieler wählen:", df_players['futwiz_id'], 
    format_func=lambda x: df_players[df_players['futwiz_id']==x]['full_name'].iloc[0])

# 2. Preise aus prices Tabelle laden
query_prices = f"SELECT timestamp, price_value FROM prices WHERE player_id = %s ORDER BY timestamp"
df_prices = pd.read_sql(query_prices, engine, params=(int(selected_player_id),))

if not df_prices.empty:
    fig = px.line(df_prices, x="timestamp", y="price_value", title="Preisverlauf")
    st.plotly_chart(fig, use_container_width=True)