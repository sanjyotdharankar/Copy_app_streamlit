import streamlit as st

st.title("📝 My Cloud Notes")

# Text area
notes = st.text_area("Write your notes below:", height=300, key="note_area")

# Copy button
if st.button("📋 Copy to Clipboard"):
    st.code(notes)  # Show the text temporarily
    st.write("Use Ctrl+C or ⌘+C to copy manually (browser limitation).")

# Save button
if st.button("💾 Save Note"):
    with open("saved_note.txt", "w") as f:
        f.write(notes)
    st.success("Note saved locally.")
