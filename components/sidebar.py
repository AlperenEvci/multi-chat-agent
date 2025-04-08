import streamlit as st
from config.constants import SESSION_KEYS, AVAILABLE_MODELS, MODEL_DESCRIPTIONS, DEFAULTS
from database import get_conversations, create_conversation, delete_conversation, get_messages

def render_sidebar():
    """Render the sidebar with navigation and settings."""
    with st.sidebar:
        # Header
        st.markdown("""
            <div class="header">
                <h1 style="color: #2196f3;">🤖 AI Assistant</h1>
                <p style="color: #666;">Your intelligent companion</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["Chat", "Image Generation"],
            format_func=lambda x: "💬 Chat" if x == "Chat" else "🎨 Image Generation"
        )
        
        if page != st.session_state.get(SESSION_KEYS["current_page"]):
            st.session_state[SESSION_KEYS["current_page"]] = page
            st.rerun()
        
        # Settings section
        st.markdown("### 🛠️ Settings")
        
        # Model selection
        selected_model = st.selectbox(
            "Choose AI Model",
            options=AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(st.session_state.get(SESSION_KEYS["selected_model"], DEFAULTS["initial_model"])),
            key="model_selector",
            format_func=lambda x: f"{x} - {MODEL_DESCRIPTIONS[x]}"
        )
        
        if selected_model != st.session_state.get(SESSION_KEYS["selected_model"]):
            st.session_state[SESSION_KEYS["selected_model"]] = selected_model
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💭 Conversations")
        
        # New conversation button
        if st.button("➕ New Conversation", key="new_conv"):
            refresh_conversations()
            num_conversations = len(st.session_state.get(SESSION_KEYS["conversations_list"], []))
            new_conv_name = f"Conversation {num_conversations + 1}"
            new_conv_id = create_conversation(name=new_conv_name)
            if new_conv_id:
                st.session_state[SESSION_KEYS["current_conversation_id"]] = new_conv_id
                st.session_state[SESSION_KEYS["messages"]] = []
                refresh_conversations()
                st.rerun()
            else:
                st.error("Failed to create new conversation. Check logs.")
        
        # Display conversations
        display_conversations()

def refresh_conversations():
    """Refresh the conversations list in session state."""
    st.session_state[SESSION_KEYS["conversations_list"]] = get_conversations()

def display_conversations():
    """Display the list of conversations in the sidebar."""
    if not st.session_state.get(SESSION_KEYS["conversations_list"]):
        refresh_conversations()
    
    if not st.session_state.get(SESSION_KEYS["conversations_list"]):
        st.info("No conversations yet. Start a new one!")
    else:
        for conv in st.session_state[SESSION_KEYS["conversations_list"]]:
            conv_id = conv["_id"]
            conv_name = conv["name"]
            
            with st.container():
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    if st.button(
                        conv_name,
                        key=f"conv_{conv_id}",
                        use_container_width=True,
                        type="primary" if conv_id == st.session_state.get(SESSION_KEYS["current_conversation_id"]) else "secondary"
                    ):
                        st.session_state[SESSION_KEYS["current_conversation_id"]] = conv_id
                        st.session_state[SESSION_KEYS["messages"]] = get_messages(conv_id)
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"del_{conv_id}", help="Delete conversation"):
                        deleted = delete_conversation(conv_id)
                        if deleted:
                            if conv_id == st.session_state.get(SESSION_KEYS["current_conversation_id"]):
                                st.session_state[SESSION_KEYS["current_conversation_id"]] = None
                                st.session_state[SESSION_KEYS["messages"]] = []
                            refresh_conversations()
                            st.rerun()
                        else:
                            st.error("Failed to delete conversation. Check logs.") 