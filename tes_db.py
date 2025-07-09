from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:password@localhost:5432/chatdb"
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)
