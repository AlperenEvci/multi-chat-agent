# Available models
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

# Page configuration
PAGE_CONFIG = {
    "page_title": "AI Assistant",
    "page_icon": "🤖",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Session state keys
SESSION_KEYS = {
    "current_page": "current_page",
    "current_conversation_id": "current_conversation_id",
    "messages": "messages",
    "conversations_list": "conversations_list",
    "selected_model": "selected_model",
    "image_history": "image_history"
}

# Default values
DEFAULTS = {
    "initial_page": "Chat",
    "initial_model": "gemini-1.5-pro",
    "num_images": 1,
    "style": "Realistic"
} 