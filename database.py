# database.py
import logging
import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from datetime import datetime
from bson import ObjectId

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    """Establishes a connection to the MongoDB database."""
    try:
        # Get MongoDB connection string from Streamlit secrets
        client = MongoClient(st.secrets["database"]["MONGO_URI"], serverSelectionTimeoutMS=5000)
        # Test the connection
        client.admin.command('ping')
        logging.info("Database connection established successfully")
        return client
    except ServerSelectionTimeoutError as e:
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

def create_conversation(name="New Conversation"):
    """Creates a new conversation and returns its ID."""
    client = get_db_connection()
    if not client:
        return None

    try:
        db = client[st.secrets["database"]["DB_NAME"]]
        conversation_data = {
            "name": name,
            "created_at": datetime.utcnow()
        }
        result = db.conversations.insert_one(conversation_data)
        logging.info(f"Created new conversation with ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logging.error(f"Error creating conversation: {e}")
        return None

def get_conversations():
    """Retrieves all conversations from the database."""
    client = get_db_connection()
    if not client:
        return []

    try:
        db = client[st.secrets["database"]["DB_NAME"]]
        conversations = list(db.conversations.find().sort("created_at", -1))
        # Convert ObjectId to string for JSON serialization
        for conv in conversations:
            conv["_id"] = str(conv["_id"])
        return conversations
    except Exception as e:
        logging.error(f"Error retrieving conversations: {e}")
        return []

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
        if conversation:
            conversation["_id"] = str(conversation["_id"])
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
        # Convert ObjectId to string for JSON serialization
        for msg in messages:
            msg["_id"] = str(msg["_id"])
        return messages
    except Exception as e:
        logging.error(f"Error retrieving messages: {e}")
        return []

def add_message(conversation_id, role, content):
    """Adds a message to a conversation."""
    client = get_db_connection()
    if not client:
        return False

    try:
        db = client[st.secrets["database"]["DB_NAME"]]
        message_data = {
            "conversation_id": ObjectId(conversation_id),
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        }
        result = db.messages.insert_one(message_data)
        logging.info(f"Added message to conversation {conversation_id}")
        return True
    except Exception as e:
        logging.error(f"Error adding message to conversation {conversation_id}: {e}")
        return False

def delete_conversation(conversation_id):
    """Deletes a conversation and its associated messages."""
    client = get_db_connection()
    if not client:
        return False

    try:
        db = client[st.secrets["database"]["DB_NAME"]]
        
        # Convert string ID to ObjectId
        conversation_oid = ObjectId(conversation_id)
        
        # Delete the conversation
        conv_result = db.conversations.delete_one({"_id": conversation_oid})
        
        # Delete associated messages
        msg_result = db.messages.delete_many({"conversation_id": conversation_oid})
        
        if conv_result.deleted_count > 0:
            logging.info(f"Deleted conversation {conversation_id} and {msg_result.deleted_count} associated messages")
            return True
        else:
            logging.warning(f"Conversation {conversation_id} not found")
            return False
    except Exception as e:
        logging.error(f"Error deleting conversation {conversation_id}: {e}")
        return False

# --- Initial Database Setup Call ---
# This will run when the module is first imported
if __name__ != "__main__": # Prevent running during direct script execution
    initialize_database() 