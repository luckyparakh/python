from fastapi import FastAPI
import psycopg.rows
import psycopg
import time
from . import models
from .database import engine
from .routes import posts, users, auth

models.Base.metadata.create_all(bind=engine)

for i in range(5):
    try:
        conn = psycopg.connect(
            "host=localhost dbname=fastapi user=postgres password=postgres")
        cursor = conn.cursor(row_factory=psycopg.rows.dict_row)
        print("Connection was successful")
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World!!!"}
