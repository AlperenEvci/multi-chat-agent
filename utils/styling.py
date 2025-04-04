def get_custom_styles():
    return """
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
    """ 