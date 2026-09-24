import os
import pandas as pd
from db_connection import get_db_engine

def load_data_to_mysql():
    engine = get_db_engine()
    
    # 1. olympics.xlsx / olympics.csv suchen und einlesen
    excel_path = os.path.join("data", "raw", "olympics.xlsx")
    if not os.path.exists(excel_path):
        excel_path = os.path.join("data", "olympics.xlsx")

    if not os.path.exists(excel_path):
        print(f"❌ Datei '{excel_path}' wurde nicht gefunden.")
        return

    print(f"⏳ Lade Hauptdaten aus {excel_path}...")
    df = pd.read_excel(excel_path)
    df.columns = [col.lower().strip() for col in df.columns]
    if "id" in df.columns:
        df = df.rename(columns={"id": "athlete_id"})

    # 2. Haupttabelle athlete_events befüllen
    if "participation_id" not in df.columns:
        df.insert(0, "participation_id", range(1, len(df) + 1))

    print("⏳ Befülle 'athlete_events'...")
    df.to_sql("athlete_events", con=engine, if_exists="replace", index=False)
    print("✅ 'athlete_events' befüllt.")

    # 3. athletes Tabelle befüllen (Eindeutige Athleten extrahieren)
    if "athlete_id" in df.columns and "name" in df.columns:
        print("⏳ Befülle 'athletes'...")
        athletes_cols = [c for c in ["athlete_id", "name", "sex", "height", "weight"] if c in df.columns]
        df_athletes = df[athletes_cols].drop_duplicates(subset=["athlete_id"])
        df_athletes.to_sql("athletes", con=engine, if_exists="replace", index=False)
        print("✅ 'athletes' befüllt.")

    # 4. events Tabelle befüllen
    if "event" in df.columns and "sport" in df.columns:
        print("⏳ Befülle 'events'...")
        df_events = df[["sport", "event"]].drop_duplicates().copy()
        df_events.insert(0, "event_id", range(1, len(df_events) + 1))
        df_events.to_sql("events", con=engine, if_exists="replace", index=False)
        print("✅ 'events' befüllt.")

    # 5. olympics / games Tabelle befüllen
    if "year" in df.columns:
        print("⏳ Befülle 'olympics'...")
        cols = [c for c in ["year", "season", "city"] if c in df.columns]
        if cols:
            df_games = df[cols].drop_duplicates()
            df_games.to_sql("olympics", con=engine, if_exists="replace", index=False)
            print("✅ 'olympics' befüllt.")

    # 6. noc_regions einlesen (falls CSV/Excel im Ordner existiert)
    noc_file = None
    for path in ["data/raw/noc_regions.csv", "data/noc_regions.csv", "data/raw/noc_regions.xlsx", "data/noc_regions.xlsx"]:
        if os.path.exists(path):
            noc_file = path
            break

    if noc_file:
        print(f"⏳ Lade NOC-Regionen aus {noc_file}...")
        df_noc = pd.read_csv(noc_file) if noc_file.endswith(".csv") else pd.read_excel(noc_file)
        df_noc.columns = [col.lower().strip() for col in df_noc.columns]
        df_noc.to_sql("noc_regions", con=engine, if_exists="replace", index=False)
        print("✅ 'noc_regions' befüllt.")
    else:
        print("ℹ️ Keine separate 'noc_regions.csv' gefunden. Erstelle minimales NOC-Mapping aus Hauptdaten...")
        if "noc" in df.columns:
            df_noc = df[["noc"]].drop_duplicates().rename(columns={"noc": "noc"})
            df_noc["region_name"] = df_noc["noc"]
            df_noc.to_sql("noc_regions", con=engine, if_exists="replace", index=False)
            print("✅ 'noc_regions' aus Hauptdaten befüllt.")

    print("All tables were successfully loaded into MySQL!")
if __name__ == "__main__":
   load_data_to_mysql()