import streamlit as st
import sqlite3

# Initialize database connection
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

# --- Delete snippet ---
def delete_snippet(snippet_id):
    c.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
    conn.commit()
    st.experimental_rerun()  # Refresh to reflect deletion

# --- Display snippets ---
st.subheader("📄 Saved Snippets")
c.execute("SELECT id, text FROM snippets ORDER BY id DESC")
snippets = c.fetchall()

if snippets:
    for sid, text in snippets:
        with st.expander(f"Snippet #{sid}"):
            st.code(text, language="python")  # or st.text(text)
            col1, col2 = st.columns([1, 1])
            with col1:
                st.button("🗑 Delete", key=f"delete_{sid}", on_click=delete_snippet, args=(sid,))
            with col2:
                st.code(text)  # can be copied manually
else:
    st.info("No snippets saved yet.")
