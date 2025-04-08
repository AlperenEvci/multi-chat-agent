# database.py
import logging
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    """Establishes a connection to the MongoDB database."""
    try:
        # Get MongoDB connection string from Streamlit secrets
        client = MongoClient(st.secrets["database"]["MONGO_URI"])
        # Test the connection
        client.admin.command('ping')
        logging.info("Database connection established successfully")
        return client
    except ConnectionError as e:
        logging.error(f"Database connection error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error while connecting to database: {e}")
        return None

def initialize_database():
    """Creates the necessary collections if they don't exist."""
    client = get_db_connection()
    if not client:
        logging.error("Cannot initialize database, connection failed.")
        return

    try:
        db = client[st.secrets["database"]["DB_NAME"]]
        
        # Create collections if they don't exist
        collections = ["conversations", "messages", "agents"]
        for collection in collections:
            if collection not in db.list_collection_names():
                db.create_collection(collection)
                logging.info(f"Created collection: {collection}")
        
        logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")

def save_conversation(conversation_data):
    """Saves a conversation to the database."""
    client = get_db_connection()
    if not client:
        return False

    try:
        db = client[st.secrets["database"]["DB_NAME"]]
        result = db.conversations.insert_one(conversation_data)
        logging.info(f"Saved conversation with ID: {result.inserted_id}")
        return True
    except Exception as e:
        logging.error(f"Error saving conversation: {e}")
        return False

def get_conversation(conversation_id):
    """Retrieves a conversation from the database."""
    client = get_db_connection()
    if not client:
        return None

    try:
        db = client[st.secrets["database"]["DB_NAME"]]
        conversation = db.conversations.find_one({"_id": conversation_id})
        return conversation
    except Exception as e:
        logging.error(f"Error retrieving conversation: {e}")
        return None

def save_message(message_data):
    """Saves a message to the database."""
    client = get_db_connection()
    if not client:
        return False

    try:
        db = client[st.secrets["database"]["DB_NAME"]]
        result = db.messages.insert_one(message_data)
        logging.info(f"Saved message with ID: {result.inserted_id}")
        return True
    except Exception as e:
        logging.error(f"Error saving message: {e}")
        return False

def get_messages(conversation_id):
    """Retrieves all messages for a conversation."""
    client = get_db_connection()
    if not client:
        return []

    try:
        db = client[st.secrets["database"]["DB_NAME"]]
        messages = list(db.messages.find({"conversation_id": conversation_id}))
        return messages
    except Exception as e:
        logging.error(f"Error retrieving messages: {e}")
        return []

# --- Initial Database Setup Call ---
# This will run when the module is first imported
if __name__ != "__main__": # Prevent running during direct script execution
    initialize_database() 