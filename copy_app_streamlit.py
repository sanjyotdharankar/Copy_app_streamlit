import streamlit as st
import sqlite3

# Initialize DB
conn = sqlite3.connect("snippets.db", check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS snippets (id INTEGER PRIMARY KEY, text TEXT)""")
conn.commit()

st.title("📋 Shared Snippet Board")

# --- Add new snippet ---
with st.form("Add Snippet"):
    snippet = st.text_area("Paste your text/code here", height=300)
    submitted = st.form_submit_button("Save")
    if submitted and snippet.strip():
        c.execute("INSERT INTO snippets (text) VALUES (?)", (snippet,))
        conn.commit()
        st.success("Snippet saved!")

# --- Display snippets ---
st.subheader("📄 Saved Snippets")
c.execute("SELECT id, text FROM snippets ORDER BY id DESC")
snippets = c.fetchall()

for idx, text in snippets:
    with st.expander(f"Snippet #{idx}", expanded=False):
        st.code(text, language="python")  # or use st.text if it's not code
        st.code(f"""{text}""")  # for actual copyable display
        st.button("Copy to Clipboard", key=f"copy_{idx}", help="Use browser to copy manually")
