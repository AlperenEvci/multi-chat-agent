# database.py
import psycopg2
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables for database connection
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# --- Connection Function ---
def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logging.info("Database connection established successfully.")
    except psycopg2.OperationalError as e:
        logging.error(f"Database connection error: {e}")
        # In a real app, you might want to handle this more gracefully
        # For Streamlit, we might let it fail and show an error in the UI
    return conn

# --- Database Initialization ---
def initialize_database():
    """Creates the necessary tables if they don't exist."""
    conn = get_db_connection()
    if not conn:
        logging.error("Cannot initialize database, connection failed.")
        return

    try:
        with conn.cursor() as cur:
            # Create conversations table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL DEFAULT 'New Conversation',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            logging.info("Checked/Created 'conversations' table.")

            # Create messages table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    conversation_id INTEGER NOT NULL,
                    role VARCHAR(50) NOT NULL, -- 'user' or 'assistant'
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
                );
            """)
            logging.info("Checked/Created 'messages' table.")

            conn.commit()
            logging.info("Database initialization complete.")
    except Exception as e:
        logging.error(f"Error initializing database tables: {e}")
        conn.rollback() # Roll back changes on error
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed after initialization.")

# --- CRUD Operations for Conversations ---

def create_conversation(name="New Conversation"):
    """Creates a new conversation and returns its ID."""
    conn = get_db_connection()
    if not conn: return None
    conversation_id = None
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO conversations (name) VALUES (%s) RETURNING id;", (name,))
            conversation_id = cur.fetchone()[0]
            conn.commit()
            logging.info(f"Created new conversation with ID: {conversation_id}")
    except Exception as e:
        logging.error(f"Error creating conversation: {e}")
        conn.rollback()
    finally:
        if conn: conn.close()
    return conversation_id

def get_conversations():
    """Retrieves all conversations, ordered by creation time."""
    conn = get_db_connection()
    if not conn: return []
    conversations = []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, created_at FROM conversations ORDER BY created_at DESC;")
            conversations = cur.fetchall()
            # Convert to list of dicts for easier use
            conversations = [
                {"id": row[0], "name": row[1], "created_at": row[2]}
                for row in conversations
            ]
    except Exception as e:
        logging.error(f"Error getting conversations: {e}")
    finally:
        if conn: conn.close()
    return conversations

def delete_conversation(conversation_id):
    """Deletes a conversation and its associated messages."""
    conn = get_db_connection()
    if not conn: return False
    success = False
    try:
        with conn.cursor() as cur:
            # CASCADE constraint should handle message deletion
            cur.execute("DELETE FROM conversations WHERE id = %s;", (conversation_id,))
            conn.commit()
            success = cur.rowcount > 0 # Check if any row was deleted
            if success:
                logging.info(f"Deleted conversation with ID: {conversation_id}")
            else:
                 logging.warning(f"Attempted to delete non-existent conversation ID: {conversation_id}")
    except Exception as e:
        logging.error(f"Error deleting conversation {conversation_id}: {e}")
        conn.rollback()
    finally:
        if conn: conn.close()
    return success

# --- CRUD Operations for Messages ---

def add_message(conversation_id, role, content):
    """Adds a message to a specific conversation."""
    conn = get_db_connection()
    if not conn: return False
    success = False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO messages (conversation_id, role, content)
                VALUES (%s, %s, %s);
            """, (conversation_id, role, content))
            conn.commit()
            success = True
            # logging.info(f"Added message to conversation {conversation_id}: {role[:10]}...") # Avoid logging full content
    except Exception as e:
        logging.error(f"Error adding message to conversation {conversation_id}: {e}")
        conn.rollback()
    finally:
        if conn: conn.close()
    return success

def get_messages(conversation_id):
    """Retrieves all messages for a specific conversation, ordered by timestamp."""
    conn = get_db_connection()
    if not conn: return []
    messages = []
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT role, content, timestamp FROM messages
                WHERE conversation_id = %s
                ORDER BY timestamp ASC;
            """, (conversation_id,))
            messages = cur.fetchall()
             # Convert to list of dicts consistent with Streamlit session state
            messages = [
                {"role": row[0], "content": row[1], "timestamp": row[2]}
                for row in messages
            ]
    except Exception as e:
        logging.error(f"Error getting messages for conversation {conversation_id}: {e}")
    finally:
        if conn: conn.close()
    return messages

# --- Initial Database Setup Call ---
# This will run when the module is first imported
if __name__ != "__main__": # Prevent running during direct script execution
    initialize_database() 