from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

app = FastAPI()

DATABASE_URL = "postgresql+psycopg2://admin:123456@localhost:5432/app"

engine = create_engine(DATABASE_URL)

@app.get("/")
def check_db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.scalar() == 1:
                return {"message": "Database connection successful"}
    except OperationalError as e:
        return {"message": str(e)}