import os
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Streamlit Cloud secrets first, .env fallback for local development
DB_HOST = st.secrets.get("DB_HOST", os.getenv("DB_HOST", "localhost"))
DB_PORT = st.secrets.get("DB_PORT", os.getenv("DB_PORT", "3306"))
DB_NAME = st.secrets.get("DB_NAME", os.getenv("DB_NAME", "olympics_db"))
DB_USER = st.secrets.get("DB_USER", os.getenv("DB_USER", "root"))
DB_PASSWORD = st.secrets.get("DB_PASSWORD", os.getenv("DB_PASSWORD"))

def get_db_engine():
    if not DB_PASSWORD:
        raise ValueError("DB_PASSWORD is not configured.")

    database_url = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    return create_engine(database_url, pool_pre_ping=True)