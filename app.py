import streamlit as st

st.set_page_config(page_title="Intuitas AI", layout="wide")

# =====================
# CUSTOM CSS
# =====================
dark_css = """
<style>
body {
    background-color: #1e1e1e;
    color: white;
}
</style>
"""

# =====================
# SIDEBAR - Folders & Previous Chats
# =====================
st.sidebar.title("📂 Folders")
st.sidebar.button("➕ New Folder")

with st.sidebar.expander("📁 General (1)", expanded=False):
    st.write("Previous Chats")
    # Placeholder for previous chat items
    st.write("• Chat 1")
    st.write("• Chat 2")

# =====================
# TOP BAR
# =====================
col1, col2, col3 = st.columns([2, 6, 3])

with col1:
    st.markdown("### **Intuitas AI** 🔍 Analyzer")

with col2:
    mode = st.radio(
        "",
        ["Normal", "Study", "Research", "Journal"],
        horizontal=True,
        label_visibility="collapsed",
    )

with col3:
    dark_mode = st.toggle("🌙 Dark Mode")
    st.button("⚙️ Settings")
    st.button("👤 Profile")

# Apply dark mode
if dark_mode:
    st.markdown(dark_css, unsafe_allow_html=True)

# =====================
# MAIN CONTENT AREA
# =====================
st.title(f"{mode} Mode")

# --- NORMAL MODE ---
if mode == "Normal":
    st.write("General purpose chat + document assistance.")
    st.text_area("💬 Ask me anything...", placeholder="Type your question here...")
    st.button("Send")

    st.subheader("Tools")
    colA, colB, colC = st.columns(3)
    with colA:
        st.button("📝 Note Maker")
    with colB:
        st.button("🧩 Clustering")
    with colC:
        st.button("🤔 Suggestive Prompts")

# --- STUDY MODE ---
elif mode == "Study":
    st.write("Tools to assist your studies.")
    tab1, tab2, tab3 = st.tabs(["Q&A", "Flashcards", "Mindmaps"])

    with tab1:
        st.text_area("Ask a Question", placeholder="Enter your study question...")
        st.button("Get Answer")

    with tab2:
        st.text_input("Flashcard Term")
        st.text_area("Definition")
        st.button("Add Flashcard")
        st.write("📚 Flashcards will appear here.")

    with tab3:
        st.text_area("Mindmap Topic", placeholder="Enter main topic...")
        st.button("Generate Mindmap")
        st.write("🧠 Mindmap visualization placeholder")

# --- RESEARCH MODE ---
elif mode == "Research":
    st.write("Advanced tools for research & analysis.")
    tab1, tab2, tab3, tab4 = st.tabs(["Web Research", "Document Analysis", "Citations", "Dashboard"])

    with tab1:
        st.text_area("Enter Topic/Query for Web Research")
        st.button("Search")

    with tab2:
        st.file_uploader("Upload Document for Analysis", type=["pdf", "docx", "txt"])
        st.button("Analyze Document")

    with tab3:
        st.text_area("Enter Source/Reference")
        st.button("Generate Citation")

    with tab4:
        st.write("📊 Research Dashboard Placeholder")
        st.write("Statistics, Graphs, and Insights here...")

# --- JOURNAL MODE ---
elif mode == "Journal":
    st.write("Keep track of your entries.")
    tab1, tab2 = st.tabs(["New Entry", "View Entries"])

    with tab1:
        st.text_input("Title")
        st.text_area("Write your journal entry...")
        st.button("Save Entry")

    with tab2:
        st.write("📓 Your previous journal entries will be displayed here.")

# =====================
# SUGGESTIVE PROMPTS
# =====================
st.subheader("💡 Suggestive Prompts")
suggestions = ["Summarize this document", "Generate key points", "Explain in simple terms"]
for s in suggestions:
    st.button(s)
