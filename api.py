from fastapi import FastAPI
import sqlite3
import os
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "snippets.db")


# --- Ensure DB and table exist ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS snippets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_db()

app = FastAPI()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/snippets")
def get_snippets():
    conn = get_db_connection()
    snippets = conn.execute("SELECT id, text FROM snippets ORDER BY id DESC").fetchall()
    conn.close()
    return [{"id": row["id"], "text": row["text"]} for row in snippets]

class Snippet(BaseModel):
    text: str

@app.post("/snippets")
def add_snippet(snippet: Snippet):
    conn = get_db_connection()
    conn.execute("INSERT INTO snippets (text) VALUES (?)", (snippet.text,))
    conn.commit()
    conn.close()
    return {"message": "Snippet added successfully"}

@app.delete("/snippets/{snippet_id}")
def delete_snippet(snippet_id: int):
    conn = get_db_connection()
    conn.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
    conn.commit()
    conn.close()
    return {"message": f"Snippet {snippet_id} deleted"}
 