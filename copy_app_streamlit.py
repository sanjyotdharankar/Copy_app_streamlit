import streamlit as st
import sqlite3

# Connect to SQLite DB
conn = sqlite3.connect("snippets.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS snippets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
)
""")
conn.commit()

st.title("📋 Shared Snippet Board")

# --- Add new snippet ---
with st.form("add_snippet_form"):
    snippet = st.text_area("Paste your text/code here", height=300)
    submitted = st.form_submit_button("Save")
    if submitted and snippet.strip():
        c.execute("INSERT INTO snippets (text) VALUES (?)", (snippet,))
        conn.commit()
        st.success("✅ Snippet saved!")

# --- Display and manage snippets ---
st.subheader("📄 Saved Snippets")
c.execute("SELECT id, text FROM snippets ORDER BY id DESC")
snippets = c.fetchall()

if snippets:
    for sid, text in snippets:
        with st.expander(f"Snippet #{sid}"):
            st.code(text, language="python")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"🗑 Delete", key=f"delete_{sid}"):
                    c.execute("DELETE FROM snippets WHERE id = ?", (sid,))
                    conn.commit()
                    st.experimental_rerun()
            with col2:
                st.code(text)
else:
    st.info("No snippets saved yet.")
