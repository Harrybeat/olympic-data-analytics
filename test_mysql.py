from src.db_connection import get_db_engine

try:
    engine = get_db_engine()

    with engine.connect() as connection:
        print("MySQL + SQLAlchemy connection successful!")

except Exception as e:
    print("Connection failed:")
    print(e)