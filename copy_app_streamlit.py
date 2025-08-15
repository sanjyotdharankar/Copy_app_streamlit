import streamlit as st
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "snippets.db")

# --- Database setup ---
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


# --- Default login credentials ---
DEFAULT_USER = "admin"
DEFAULT_PASS = "pass123"

# --- Session state for login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login(username, password):
    if username == DEFAULT_USER and password == DEFAULT_PASS:
        st.session_state.logged_in = True
    else:
        st.error("❌ Invalid username or password")

# --- Login UI ---
if not st.session_state.logged_in:
    st.title("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        login(user, pwd)
    st.stop()

# --- Main UI ---
st.title("📋To-Do List Board")

# --- Add snippet form ---
with st.form("add_snippet_form"):
    snippet = st.text_area("📝 Paste your text", height=200)
    submitted = st.form_submit_button("➕ Add Snippet")
    if submitted and snippet.strip():
        c.execute("INSERT INTO snippets (text) VALUES (?)", (snippet,))
        conn.commit()
        st.success("✅ Snippet added!")
        st.rerun()

# --- Display snippets as to-do style cards ---
st.subheader("🗂️ Saved Tasks ")

c.execute("SELECT id, text FROM snippets ORDER BY id DESC")
snippets = c.fetchall()

if not snippets:
    st.info("No snippets saved yet.")
else:
    for sid, text in snippets:
        with st.container():
            st.markdown(f"**🧾 Snippet #{sid}**")
            st.code(text, language="python")
            cols = st.columns([1, 1])
            with cols[0]:
                if st.button("🗑 Delete", key=f"delete_{sid}"):
                    c.execute("DELETE FROM snippets WHERE id = ?", (sid,))
                    conn.commit()
                    st.rerun()
            with cols[1]:
                st.code(text)
        st.markdown("---")
