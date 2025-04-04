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
from utils.styling import get_custom_styles
from config.constants import PAGE_CONFIG, SESSION_KEYS, DEFAULTS
from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface
from components.image_generation import render_image_generation_interface

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set page configuration
st.set_page_config(**PAGE_CONFIG)

# Apply custom styles
st.markdown(get_custom_styles(), unsafe_allow_html=True)

# Initialize session state
if SESSION_KEYS["current_page"] not in st.session_state:
    st.session_state[SESSION_KEYS["current_page"]] = DEFAULTS["initial_page"]

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

# Render sidebar
render_sidebar()

# Get the agent executor based on the selected model
agent_executor = setup_agent(st.session_state.get(SESSION_KEYS["selected_model"], DEFAULTS["initial_model"]))

# Render main content based on current page
if st.session_state[SESSION_KEYS["current_page"]] == "Chat":
    render_chat_interface(agent_executor)
else:
    render_image_generation_interface() 