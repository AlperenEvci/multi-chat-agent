# app.py
import streamlit as st
from agent import create_agent_executor
# Import database functions
from database import (
    get_conversations,
    create_conversation,
    get_messages,
    add_message,
    delete_conversation
)
import sys
import logging # Import logging
import time
# Import message types for chat history
from langchain_core.messages import HumanMessage, AIMessage
# Import NEW image generation functions for Imagen
from image_generation import (
    setup_image_generator, 
    generate_images_with_imagen, 
    process_imagen_response
)

# --- Custom Theme Configuration ---
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    /* Global styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container styling */
    .main {
        background: #1a1a1a;
        color: #ffffff;
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: #2d2d2d;
        color: #ffffff;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: #3d3d3d !important;
        color: #ffffff !important;
        border: 1px solid #4d4d4d !important;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #2196f3 !important;
    }
    
    /* Dropdown menu styling */
    .stSelectbox > div > div > div[data-baseweb="select"] > div {
        background: #3d3d3d !important;
        color: #ffffff !important;
    }
    
    /* Dropdown options styling */
    div[data-baseweb="popover"] * {
        background: #3d3d3d !important;
        color: #ffffff !important;
    }
    
    div[data-baseweb="popover"] div[role="option"]:hover {
        background: #4d4d4d !important;
    }
    
    /* Settings text color */
    .sidebar .block-container {
        color: #ffffff;
    }
    
    /* Headers in sidebar */
    .sidebar h1, .sidebar h2, .sidebar h3 {
        color: #ffffff !important;
    }
    
    /* Paragraph text in sidebar */
    .sidebar p {
        color: #cccccc !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        color: white;
        border: none;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background: #2d2d2d;
        color: #ffffff;
    }
    
    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
    }
    
    .stChatMessage[data-testid="assistant"] {
        background: linear-gradient(135deg, #3d3d3d 0%, #2d2d2d 100%);
    }
    
    /* Chat input styling */
    .stChatInput, .stTextInput>div>div>input {
        background: #3d3d3d !important;
        color: #ffffff !important;
        border: 1px solid #4d4d4d !important;
    }
    
    .stChatInput:focus, .stTextInput>div>div>input:focus {
        border-color: #2196f3 !important;
        box-shadow: 0 0 0 2px rgba(33,150,243,0.2) !important;
    }
    
    /* Header styling */
    .header {
        background: #2d2d2d;
        color: #ffffff;
    }
    
    .header h1, .header h2 {
        color: #2196f3 !important;
        -webkit-background-clip: initial;
        -webkit-text-fill-color: initial;
    }
    
    .header p {
        color: #cccccc !important;
    }
    
    /* Model card styling */
    .model-card {
        background: #2d2d2d;
        border: 1px solid #4d4d4d;
        color: #ffffff;
    }
    
    /* Conversation card styling */
    .conversation-card {
        background: #2d2d2d;
        border: 1px solid #4d4d4d;
        color: #ffffff;
    }
    
    /* Form styling */
    .stForm {
        background: #2d2d2d;
        color: #ffffff;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background: #3d3d3d !important;
        color: #ffffff !important;
        border: 1px solid #4d4d4d !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #4d4d4d !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-track {
        background: #2d2d2d;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4d4d4d;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #5d5d5d;
    }
    
    /* Radio button styling */
    .stRadio > div {
        color: #ffffff !important;
    }
    
    /* Markdown text color */
    .stMarkdown {
        color: #ffffff;
    }
    
    /* Info, Success, Error message styling */
    .stSuccess, .stInfo, .stError {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Available Models ---
AVAILABLE_MODELS = [
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-2.5-pro-exp-03-25",
    "deepseek-chat",    # DeepSeek Chat
    "deepseek-coder",   # DeepSeek Coder
    "gemma",            # Google Gemma 3 4B
]

# Model descriptions
MODEL_DESCRIPTIONS = {
    "gemini-1.5-pro": "Google's advanced model for complex tasks",
    "gemini-1.5-flash": "Fast and efficient for quick responses",
    "gemini-2.5-pro-exp-03-25": "Latest experimental version with enhanced capabilities",
    "deepseek-chat": "Specialized for general conversation",
    "deepseek-coder": "Optimized for programming and technical tasks",
    "gemma": "Google's lightweight but powerful model"
}

# --- Page Selection ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Chat"

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("""
        <div class="header">
            <h1 style="color: #2196f3;">🤖 AI Assistant</h1>
            <p style="color: #666;">Your intelligent companion</p>
        </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["Chat", "Image Generation"],
        format_func=lambda x: "💬 Chat" if x == "Chat" else "🎨 Image Generation"
    )
    
    if page != st.session_state.current_page:
        st.session_state.current_page = page
        st.rerun()

# --- Agent Setup ---
# Cache the agent executor based on the selected model
@st.cache_resource
def setup_agent(model_name: str):
    try:
        agent_executor = create_agent_executor(model_name=model_name)
        logging.info(f"Agent Executor created for Streamlit app with model: {model_name}")
        return agent_executor
    except Exception as e:
        st.error(f"Failed to initialize the agent with model {model_name}: {e}")
        logging.error(f"Error in setup_agent({model_name}): {e}")
        return None

# --- Main App Content ---
if st.session_state.current_page == "Chat":
    # --- Chat Interface ---
    st.markdown("""
        <div class="header">
            <h2 style="color: #2196f3;">💬 AI Chat</h2>
            <p style="color: #666;">Ask anything to your AI assistant</p>
        </div>
    """, unsafe_allow_html=True)

    # --- Session State Initialization ---
    if 'current_conversation_id' not in st.session_state:
        st.session_state.current_conversation_id = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversations_list' not in st.session_state:
        st.session_state.conversations_list = []
    if 'selected_model' not in st.session_state or st.session_state.selected_model not in AVAILABLE_MODELS:
        st.session_state.selected_model = AVAILABLE_MODELS[0]

    # --- Helper function to refresh conversations list ---
    def refresh_conversations():
        st.session_state.conversations_list = get_conversations()

    # --- Model Selection ---
    with st.sidebar:
        st.markdown("### 🛠️ Settings")
        
        # Model selection with description
        selected_model = st.selectbox(
            "Choose AI Model",
            options=AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(st.session_state.selected_model),
            key="model_selector",
            format_func=lambda x: f"{x} - {MODEL_DESCRIPTIONS[x]}"
        )

        if selected_model != st.session_state.selected_model:
            st.session_state.selected_model = selected_model
            st.rerun()

        st.markdown("---")
        st.markdown("### 💭 Conversations")

        # Button to create a new conversation
        if st.button("➕ New Conversation", key="new_conv"):
            refresh_conversations()
            num_conversations = len(st.session_state.conversations_list)
            new_conv_name = f"Conversation {num_conversations + 1}"
            new_conv_id = create_conversation(name=new_conv_name)
            if new_conv_id:
                st.session_state.current_conversation_id = new_conv_id
                st.session_state.messages = []
                refresh_conversations()
                st.rerun()
            else:
                st.error("Failed to create new conversation. Check logs.")

        # Refresh and display list of conversations
        if not st.session_state.conversations_list:
            refresh_conversations()

        if not st.session_state.conversations_list:
            st.info("No conversations yet. Start a new one!")
        else:
            for conv in st.session_state.conversations_list:
                conv_id = conv["id"]
                conv_name = conv["name"]
                
                # Create a container for each conversation
                with st.container():
                    col1, col2 = st.columns([0.8, 0.2])
                    with col1:
                        if st.button(
                            conv_name,
                            key=f"conv_{conv_id}",
                            use_container_width=True,
                            type="primary" if conv_id == st.session_state.current_conversation_id else "secondary"
                        ):
                            st.session_state.current_conversation_id = conv_id
                            st.session_state.messages = get_messages(conv_id)
                            st.rerun()
                    with col2:
                        if st.button("🗑️", key=f"del_{conv_id}", help="Delete conversation"):
                            deleted = delete_conversation(conv_id)
                            if deleted:
                                if conv_id == st.session_state.current_conversation_id:
                                    st.session_state.current_conversation_id = None
                                    st.session_state.messages = []
                                refresh_conversations()
                                st.rerun()
                            else:
                                st.error(f"Failed to delete conversation {conv_id}")

    # --- Get the agent executor based on the selected model ---
    agent_executor = setup_agent(st.session_state.selected_model)

    # --- Main Chat Area ---
    if st.session_state.current_conversation_id:
        if not st.session_state.messages:
            st.session_state.messages = get_messages(st.session_state.current_conversation_id)

        # Display chat messages with improved styling
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        st.info("Select a conversation or start a new one from the sidebar.")

    # Accept user input with improved styling
    if prompt := st.chat_input("What do you want to ask the agent?"):
        if not st.session_state.current_conversation_id:
            st.error("Please select or start a new conversation first!")
        elif not agent_executor:
            st.error(f"Agent could not be initialized for model '{st.session_state.selected_model}'. Please check the logs.")
        else:
            # Add user message to DB and display immediately
            add_message(st.session_state.current_conversation_id, "user", prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get agent response with loading animation
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    try:
                        chat_history_for_prompt = []
                        raw_messages_for_history = st.session_state.messages[:-1]
                        for msg in raw_messages_for_history:
                            if msg["role"] == "user":
                                chat_history_for_prompt.append(HumanMessage(content=msg["content"]))
                            elif msg["role"] == "assistant":
                                chat_history_for_prompt.append(AIMessage(content=msg["content"]))

                        response = agent_executor.invoke({
                            "input": prompt,
                            "chat_history": chat_history_for_prompt
                        })
                        response_content = response.get('output', 'Sorry, I had trouble processing that.')

                    except Exception as e:
                        response_content = f"An error occurred during agent processing: {e}"
                        logging.exception("Error during agent invocation:")

                    # Add agent response to DB and display
                    add_message(st.session_state.current_conversation_id, "assistant", response_content)
                    st.markdown(response_content)
                    st.session_state.messages.append({"role": "assistant", "content": response_content})

else:
    # --- Image Generation Interface (Now using Imagen via AI Platform) ---
    st.markdown("""
        <div class="header">
            <h2 style="color: #2196f3;">🎨 Image Generation</h2>
            <p style="color: #666;">Create amazing images with AI</p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state for image history
    if 'image_history' not in st.session_state:
        st.session_state.image_history = []

    # Setup the image generator (checks AI Platform init)
    imagen_ready = setup_image_generator()

    if not imagen_ready:
        # Error messages are now handled within setup_image_generator
        # It will show specific errors like missing project ID or library
        pass # Prevent Streamlit from crashing if setup fails
    else:
        # Image generation form with improved styling
        with st.form("image_generation_form"):
            st.markdown("### 🎯 Image Description")
            prompt = st.text_area(
                "Describe the image you want to generate",
                placeholder="A photorealistic cat wearing sunglasses...",
                height=100
            )
            
            st.markdown("### ⚙️ Generation Settings")
            col1, col2 = st.columns(2)
            with col1:
                num_images = st.number_input(
                    "Number of images",
                    min_value=1,
                    max_value=8,
                    value=1,
                    help="How many variations to generate"
                )
            with col2:
                style = st.selectbox(
                    "Image Style",
                    ["Realistic", "Photographic", "Artistic", "Cartoon", "Abstract", "Watercolor", "Oil Painting"],
                    help="The artistic style of the generated images"
                )
            
            submitted = st.form_submit_button("✨ Generate Images")

        if submitted and prompt:
            with st.spinner("🎨 Creating your images..."):
                try:
                    api_response = generate_images_with_imagen(
                        prompt=prompt,
                        num_images=num_images,
                        style=style
                    )
                    
                    if api_response:
                        processed_images = process_imagen_response(api_response)
                    else:
                        processed_images = None
                    
                    if processed_images:
                        st.session_state.image_history.append({
                            "prompt": prompt,
                            "style": style,
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                        st.success(f"✨ Successfully generated {len(processed_images)} image(s)!")
                        
                        # Display images in a grid with improved styling
                        cols = st.columns(len(processed_images))
                        for idx, (col, img) in enumerate(zip(cols, processed_images)):
                            with col:
                                st.image(img, caption=f"Image {idx + 1}")
                    else:
                        st.warning("Failed to generate or process images. Check the logs for details.")
                
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    logging.exception("Error in image generation:")

        # Display image generation history with improved styling
        if st.session_state.image_history:
            st.markdown("### 📜 Generation History")
            for entry in reversed(st.session_state.image_history):
                with st.expander(f"🎨 {entry['prompt']} ({entry['style']})"):
                    st.write(f"⏰ Generated at: {entry['timestamp']}") 