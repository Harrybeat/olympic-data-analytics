import os
from sqlalchemy import text
from db_connection import get_db_engine

def create_tables():
    sql_file_path = os.path.join("sql", "01_schema.sql")
    
    if not os.path.exists(sql_file_path):
        print(f"❌ Fehler: Datei '{sql_file_path}' wurde nicht gefunden.")
        return

    with open(sql_file_path, "r", encoding="utf-8") as file:
        sql_script = file.read()

    engine = get_db_engine()
    with engine.begin() as conn:
        conn.execute(text(sql_script))
        
    print("✅ Tabellenschema aus sql/01_schema.sql wurde erfolgreich in 'olympics_db' ausgeführt!")

if __name__ == "__main__":
    create_tables()