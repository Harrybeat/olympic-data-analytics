import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Füge 'src' zum Python-Pfad hinzu, um db_connection zu nutzen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from db_connection import get_db_engine

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Olympic Data Analytics Dashboard",
    page_icon="🥇",
    layout="wide"
)

# --- DATABASE CONNECTION ---
@st.cache_resource
def get_connection():
    return get_db_engine()

engine = get_connection()

# --- TITLE ---
st.title("🥇 Olympic Games Data Analytics Dashboard")
st.markdown("Interaktive Auswertung historischer Olympischer Spiele direkt aus PostgreSQL.")

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filter")

@st.cache_data
def load_filter_options():
    with engine.connect() as conn:
        df_years = pd.read_sql("SELECT DISTINCT year FROM athlete_events ORDER BY year DESC", conn)
        df_nocs = pd.read_sql("SELECT DISTINCT noc FROM athlete_events WHERE noc IS NOT NULL ORDER BY noc", conn)
    return df_years['year'].tolist(), df_nocs['noc'].tolist()

try:
    all_years, all_nocs = load_filter_options()
except Exception as e:
    st.error(f"Fehler bei der Verbindung zur Datenbank: {e}")
    st.stop()

selected_year = st.sidebar.selectbox("Jahr auswählen (optional)", ["Alle Jahre"] + all_years)
selected_noc = st.sidebar.multiselect("NOC / Länder auswählen", options=all_nocs, default=["USA", "GER", "CHN"])

# --- DATA RETRIEVAL ---
year_condition = f"AND year = {selected_year}" if selected_year != "Alle Jahre" else ""

# Query 1: Top Medaillenspiegel
query_medals = f"""
    SELECT 
        noc,
        COUNT(CASE WHEN medal = 'Gold' THEN 1 END) AS gold,
        COUNT(CASE WHEN medal = 'Silver' THEN 1 END) AS silber,
        COUNT(CASE WHEN medal = 'Bronze' THEN 1 END) AS bronze,
        COUNT(medal) AS gesamt
    FROM athlete_events
    WHERE medal IS NOT NULL {year_condition}
    GROUP BY noc
    ORDER BY gold DESC, silber DESC, bronze DESC
    LIMIT 15;
"""

# Query 2: Geschlechterverteilung
query_gender = """
    SELECT 
        year,
        COUNT(CASE WHEN sex = 'M' THEN 1 END) AS maenner,
        COUNT(CASE WHEN sex = 'F' THEN 1 END) AS frauen
    FROM athlete_events
    GROUP BY year
    ORDER BY year ASC;
"""

# Query 3: Medaillen im Zeitverlauf
noc_clause = "','".join(selected_noc) if selected_noc else ""
query_trend = f"""
    SELECT 
        year,
        noc,
        COUNT(medal) AS medaillen
    FROM athlete_events
    WHERE medal IS NOT NULL AND noc IN ('{noc_clause}')
    GROUP BY year, noc
    ORDER BY year ASC;
"""

with engine.connect() as conn:
    df_medals = pd.read_sql(query_medals, conn)
    df_gender = pd.read_sql(query_gender, conn)
    df_trend = pd.read_sql(query_trend, conn) if noc_clause else pd.DataFrame()
    
    total_athletes = pd.read_sql("SELECT COUNT(DISTINCT athlete_id) FROM athlete_events", conn).iloc[0, 0]
    total_events = pd.read_sql("SELECT COUNT(DISTINCT event) FROM athlete_events", conn).iloc[0, 0]
    total_medals = pd.read_sql("SELECT COUNT(*) FROM athlete_events WHERE medal IS NOT NULL", conn).iloc[0, 0]

# --- METRICS ROW ---
col1, col2, col3 = st.columns(3)
col1.metric("Gesamte Athleten", f"{total_athletes:,}")
col2.metric("Disziplinen / Events", f"{total_events:,}")
col3.metric("Vergebene Medaillen", f"{total_medals:,}")

st.divider()

# --- CHARTS SECTION ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("🏆 Top 15 Medaillenspiegel")
    if not df_medals.empty:
        fig_medals = px.bar(
            df_medals, 
            x='noc', 
            y=['gold', 'silber', 'bronze'], 
            title="Medaillen nach Land",
            labels={'value': 'Anzahl Medaillen', 'noc': 'Land (NOC)'},
            color_discrete_map={'gold': '#FFD700', 'silber': '#C0C0C0', 'bronze': '#CD7F32'}
        )
        st.plotly_chart(fig_medals, use_container_width=True)
    else:
        st.info("Keine Daten vorhanden.")

with c2:
    st.subheader("📈 Medaillenentwicklung im Zeitverlauf")
    if not df_trend.empty:
        fig_trend = px.line(
            df_trend, 
            x='year', 
            y='medaillen', 
            color='noc',
            markers=True,
            title="Medaillen-Trend pro Land"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Bitte wähle mindestens ein Land aus.")

st.divider()

# Geschlechterverteilung Chart
st.subheader("👥 Entwicklung der Geschlechterverteilung (1896 – Heute)")
fig_gender = px.area(
    df_gender, 
    x='year', 
    y=['maenner', 'frauen'],
    labels={'value': 'Anzahl Athleten', 'year': 'Jahr'},
    color_discrete_map={'maenner': '#1f77b4', 'frauen': '#e377c2'}
)
st.plotly_chart(fig_gender, use_container_width=True)