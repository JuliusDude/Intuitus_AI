import streamlit as st
import datetime

st.set_page_config(page_title="Intuitas AI", layout="wide")

# Session State initialization
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = None
if 'notes' not in st.session_state:
    st.session_state.notes = []
if 'current_note' not in st.session_state:
    st.session_state.current_note = None
if 'show_mode_selector' not in st.session_state:
    st.session_state.show_mode_selector = False

# =====================
# CUSTOM CSS
# =====================
custom_css = """
<style>
    .note-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 10px 0;
        cursor: pointer;
    }
    .mode-selector {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 20px 0;
    }
    .sidebar-note {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        cursor: pointer;
    }
    div[data-testid="stSidebarNav"] {
        background-color: #f9f9f9;
    }
    /* Chat container styles */
    .chat-container {
        height: 400px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #f8f9fa;
        scroll-behavior: smooth;
    }
    .chat-message {
        margin: 10px 0;
        padding: 10px 15px;
        border-radius: 15px;
        max-width: 80%;
        word-wrap: break-word;
        position: relative;
        clear: both;
    }
    .user-message {
        background-color: #e3f2fd;
        float: right;
        border-bottom-right-radius: 5px;
    }
    .bot-message {
        background-color: white;
        float: left;
        border-bottom-left-radius: 5px;
    }
    /* Chat input styling */
    [data-testid="stTextInput"] {
        background-color: white;
        border-radius: 20px !important;
        padding: 5px 15px !important;
        margin-bottom: 0 !important;
    }
    .send-button {
        background-color: #2196f3;
        color: white;
        border-radius: 50%;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        border: none;
        margin-top: 5px;
    }
    /* Summary section */
    .summary-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    /* View toggle buttons */
    .view-toggle {
        display: inline-block;
        padding: 5px 15px;
        margin: 0 5px;
        border-radius: 20px;
        cursor: pointer;
        border: 1px solid #ddd;
    }
    .view-toggle.active {
        background-color: #e3f2fd;
        border-color: #90caf9;
    }
    /* Tools section */
    .tools-section {
        margin-top: 20px;
        border-top: 1px solid #ddd;
        padding-top: 10px;
    }
    /* Mind Map styles */
    .mind-map-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .mind-map-node {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 5px 10px;
        margin: 5px 0;
        display: inline-block;
    }
    .mind-map-center {
        background: #e3f2fd;
        font-weight: bold;
    }
</style>
"""

# Add JavaScript for Enter key handling and auto-scroll
js_code = """
<script>
// Handle Enter key for submission
document.addEventListener('keydown', function(e) {
    if (e.target.tagName.toLowerCase() === 'textarea' || e.target.tagName.toLowerCase() === 'input') {
        if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) {
            e.preventDefault();
            // Find and click the closest send button
            const sendButton = e.target.closest('.chat-input-container').querySelector('.send-button');
            if (sendButton) {
                sendButton.click();
            }
        }
    }
});

// Auto-scroll chat to bottom
function scrollChatToBottom() {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// Call scroll function after content updates
const observer = new MutationObserver(scrollChatToBottom);
const chatContainer = document.querySelector('.chat-container');
if (chatContainer) {
    observer.observe(chatContainer, { childList: true, subtree: true });
}

// Initial scroll
scrollChatToBottom();
</script>
"""

# =====================
# Helper Functions
# =====================
def create_new_note(title, mode):
    new_note = {
        'id': len(st.session_state.notes),
        'title': title,
        'mode': mode,
        'date': datetime.datetime.now().strftime("%b %d, %Y"),
        'chat_content': "",
        'summary_content': "",
        'sources': []
    }
    st.session_state.notes.append(new_note)
    st.session_state.current_note = new_note
    st.session_state.show_mode_selector = False

def show_note_content(note):
    st.title(note['title'])
    st.caption(f"{note['mode']} Mode • Created {note['date']}")
    
    # Sources section with counter
    source_count = len(note.get('sources', []))
    with st.expander(f"📚 Sources ({source_count})", expanded=False):
        uploaded_files = st.file_uploader("Add sources", type=["pdf", "docx", "txt"], accept_multiple_files=True, key=f"sources_{note['id']}")
        if uploaded_files:
            note['sources'] = uploaded_files
            
    # View selector with buttons
    col1, col2 = st.columns([1, 4])
    with col1:
        chat_btn = st.button("💬 Chat", key=f"chat_btn_{note['id']}", use_container_width=True)
        summary_btn = st.button("📝 Summary", key=f"summary_btn_{note['id']}", use_container_width=True)
    
    # Update view mode based on button clicks
    if 'view_mode' not in note:
        note['view_mode'] = 'chat'
    if chat_btn:
        note['view_mode'] = 'chat'
    if summary_btn:
        note['view_mode'] = 'summary'
    
    with col2:
        if note['view_mode'] == 'chat':
            # Initialize messages list if not exists
            if 'messages' not in note:
                note['messages'] = []
            
            # Chat display container
            st.markdown('<div class="chat-container" id="chat-messages">', unsafe_allow_html=True)
            for msg in note.get('messages', []):
                if msg['type'] == 'user':
                    st.markdown(f'<div class="chat-message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message bot-message">{msg["content"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Chat input area with dynamic key based on message count
            message_count = len(note.get('messages', []))
            with st.container():
                input_cols = st.columns([6, 1])
                with input_cols[0]:
                    message = st.text_input(
                        "Message",
                        key=f"chat_input_{note['id']}_{message_count}",
                        placeholder="Type your message...",
                        label_visibility="collapsed"
                    )
                with input_cols[1]:
                    send = st.button("➤", key=f"send_{note['id']}_{message_count}")

                if send and message:
                    note['messages'].append({"type": "user", "content": message})
                    note['messages'].append({"type": "bot", "content": "This is a sample response. Replace with actual AI response."})
                    st.rerun()
                
        else:
            # Summary view
            st.markdown('<div class="summary-container">', unsafe_allow_html=True)
            if source_count > 0:
                st.markdown("### Document Summary")
                # Add actual summary generation logic here
                st.write("Summary of uploaded documents will appear here.")
            else:
                st.info("📝 Upload documents to see their summary here")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Tools section as expandable button
    with st.expander("🛠️ Tools", expanded=False):
        tool_cols = st.columns(4)
        with tool_cols[0]:
            st.button("📝 Note Maker", key=f"tool_note_{note['id']}")
        with tool_cols[1]:
            st.button("🧩 Clustering", key=f"tool_cluster_{note['id']}")
        with tool_cols[2]:
            if st.button("� Mind Map", key=f"tool_mind_{note['id']}"):
                if not note.get('mind_map_active'):
                    note['mind_map_active'] = True
                    note['mind_map_data'] = {"center": "Main Topic", "nodes": []}
        with tool_cols[3]:
            st.button("�🤔 Suggestive Prompts", key=f"tool_prompt_{note['id']}")
        
        # Mind Map Section
        if note.get('mind_map_active'):
            st.markdown("### 🧠 Mind Map Builder")
            col1, col2 = st.columns([3, 1])
            with col1:
                # Main topic input
                new_topic = st.text_input("Add Topic", 
                                        key=f"mind_topic_{note['id']}", 
                                        placeholder="Enter a topic...")
                # Display current mind map structure
                st.markdown("#### Current Mind Map")
                # Display mind map as a tree structure
                def display_mind_map(data):
                    st.markdown(f"**Center:** {data['center']}")
                    if data['nodes']:
                        for idx, node in enumerate(data['nodes']):
                            st.markdown(f"  {'  ' * 1}• {node}")
                
                display_mind_map(note['mind_map_data'])
            
            with col2:
                if st.button("Add Topic", key=f"add_topic_{note['id']}") and new_topic:
                    note['mind_map_data']['nodes'].append(new_topic)
                if st.button("Clear Map", key=f"clear_mind_{note['id']}"):
                    note['mind_map_data'] = {"center": "Main Topic", "nodes": []}

# =====================
# Sidebar - Notes List
# =====================
with st.sidebar:
    st.title("Intuitus AI")
    if st.button("➕ New Note"):
        st.session_state.show_mode_selector = True
        st.session_state.current_note = None
    
    st.divider()
    st.subheader("Your Notes")
    for note in st.session_state.notes:
        if st.button(
            f"{note['title']}\n{note['mode']} • {note['date']}", 
            key=f"note_{note['id']}", 
            use_container_width=True
        ):
            st.session_state.current_note = note
            st.session_state.show_mode_selector = False

# =====================
# Main Content Area
# =====================

# Apply custom CSS and JavaScript
st.markdown(custom_css + js_code, unsafe_allow_html=True)

# Show mode selector when creating new note
if st.session_state.show_mode_selector:
    st.title("Create New Note")
    
    note_title = st.text_input("Note Title", placeholder="Enter a title for your note...")
    
    st.subheader("Select Mode")
    mode_cols = st.columns(4)
    
    modes = {
        "Normal": "🔍 General purpose note taking and analysis",
        "Study": "📚 Organized study notes and learning",
        "Research": "🔬 In-depth research and analysis"
    }
    
    for i, (mode, description) in enumerate(modes.items()):
        with mode_cols[i]:
            if st.button(f"{mode}\n{description}", use_container_width=True):
                if note_title:  # Only create if title is provided
                    create_new_note(note_title, mode)
                else:
                    st.error("Please enter a title for your note")

# Show current note if selected
elif st.session_state.current_note:
    show_note_content(st.session_state.current_note)
    
# Show notes overview if nothing is selected
else:
    st.title("Your Notes")
    
    # Create columns for the note cards
    cols = st.columns(3)
    for i, note in enumerate(st.session_state.notes):
        with cols[i % 3]:
            # Create a clickable card for each note
            card_html = f"""
            <div class="note-card" onclick="alert('clicked')">
                <h3>{note['title']}</h3>
                <p>{note['mode']} • {note['date']}</p>
            </div>
            """
            if st.markdown(card_html, unsafe_allow_html=True):
                st.session_state.current_note = note
                st.session_state.show_mode_selector = False
    
    # Show create new note button
    if not st.session_state.notes:
        st.write("No notes yet. Click '➕ New Note' to get started!")
