import streamlit as st
import pandas as pd
import plotly.express as px
from fut_dashboard import engine

st.set_page_config(page_title="Rating Analyse", layout="wide")
st.title("Rating-Markt-Analyse")

# Rating wählbar machen über side bar
available_ratings = pd.read_sql("SELECT DISTINCT rating FROM rating_snapshots ORDER BY rating ASC", engine)
if not available_ratings.empty:
    selected_rating = st.sidebar.select_slider(
        "Rating wählen:", 
        options=available_ratings['rating'].tolist(),
        value=available_ratings['rating'].iloc[0]
    )
else:
    st.error("Keine Snapshot-Daten gefunden.")
    st.stop()

query_latest = """
    SELECT rank, price_value, timestamp 
    FROM rating_snapshots 
    WHERE rating = %s 
    AND timestamp = (SELECT MAX(timestamp) FROM rating_snapshots WHERE rating = %s)
    ORDER BY rank ASC
"""
sql_params = (selected_rating, selected_rating)
df_latest = pd.read_sql(query_latest, engine, params=sql_params)

query_trend = """
    SELECT timestamp, price_value 
    FROM rating_snapshots 
    WHERE rating = %s AND rank = 3
    ORDER BY timestamp ASC
"""
sql_params = (selected_rating,)
df_trend = pd.read_sql(query_trend, engine, params=sql_params)

# Teil 1: Aktueller (Richt-)Preis & Entwicklung innerhalb 24h
if not df_trend.empty:
    current_price = df_trend['price_value'].iloc[-1]

    last_price = df_trend['price_value'].iloc[-97] if len(df_trend) > 96 else current_price
    delta = int(current_price - last_price)
    
    st.metric(label=f"Aktueller Richtpreis (Rating {selected_rating} | Rank 3)", 
              value=f"{int(current_price):,}".replace(",", "."), 
              delta=f"{delta:,}".replace(",", ".")
    )

# Teil 2: Der Preisverlauf
st.write(f"### Preisverlauf {selected_rating}er")
if not df_trend.empty:
    fig_line = px.line(df_trend, x="timestamp", y="price_value", line_shape="hv")
    fig_line.update_traces(line_color='#00CC96', line_width=3)
    st.plotly_chart(fig_line, use_container_width=True)

# Teil 3: Aktuelle Verteilung der 10 günstigsten (bei hohen ratings interessant)
st.write(f"### Aktueller Snapshot Verteilung")
if not df_latest.empty:
    fig_bar = px.bar(df_latest, x="rank", y="price_value", 
                     color="price_value",
                     labels={"rank": "Rank", "price_value": "Preis"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("Keine Snapshot-Details verfügbar.")
