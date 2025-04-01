# AI Agent with Multi-Model Chat & Image Generation

This project implements a conversational AI agent using Python, Streamlit, and LangChain. It features:

- **Multi-Model Support:** Easily switch between different large language models (LLMs) from various providers like Google (Gemini) and Groq (Llama 3).
- **Conversational Interface:** Chat with the AI agent through a user-friendly Streamlit web interface.
- **Persistent Conversations:** Chat history is saved to a PostgreSQL database, allowing you to resume conversations later.
- **Agent Tools:** The agent can use tools like Web Search (DuckDuckGo) and a Python REPL to answer questions and perform tasks.
- **Image Generation:** A separate page allows generating images using Google Cloud's Imagen model via the Vertex AI API.

## Features

- **Model Selection:** Choose your preferred LLM from a dropdown list in the sidebar.
- **Conversation Management:** Start new conversations, switch between existing ones, and delete old conversations.
- **Database Persistence:** Uses PostgreSQL to store conversation history (conversation metadata and individual messages).
- **Web Search Tool:** The agent can search the web to find up-to-date information.
- **Python REPL Tool:** The agent can execute Python code to perform calculations or other tasks.
- **Imagen Image Generation:** Generate images based on text prompts and style selections using Google's Imagen model.
- **Modular Design:** Code is organized into separate files for the agent logic (`agent.py`), tools (`tools.py`), web app (`app.py`), database interactions (`database.py`), and image generation (`image_generation.py`).

## Tech Stack

- **Python 3.x**
- **Streamlit:** For the web interface.
- **LangChain:** Framework for building LLM applications (agents, prompts, tools).
- **LangChain Providers:**
  - `langchain-google-genai` (for Gemini models)
  - `langchain-groq` (for Llama 3 via Groq API)
- **Google Cloud AI Platform:** For Imagen image generation (`google-cloud-aiplatform`).
- **PostgreSQL:** Relational database for storing conversations.
- `psycopg2-binary`: Python adapter for PostgreSQL.
- `python-dotenv`: For managing environment variables (API keys, DB credentials).
- `langchainhub`: To pull standard LangChain prompt templates.
- `langchain-experimental`: For experimental tools like `PythonREPLTool`.
- `duckduckgo-search`: For the web search tool.

## Setup

**1. Prerequisites:**

- Python 3.8+ installed.
- PostgreSQL server running and accessible.
- Google Cloud SDK (`gcloud` CLI) installed ([installation guide](https://cloud.google.com/sdk/docs/install)) for Imagen authentication.
- API Keys:
  - Google AI API Key (for Gemini models)
  - Groq API Key (for Llama 3 models)
- Google Cloud Project set up with Vertex AI API enabled (for Imagen).

**2. Clone the Repository:**

```bash
git clone <your-repository-url>
cd <repository-directory>
```

**3. Create a Virtual Environment:**

```bash
python -m venv venv
# Activate the environment
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Windows (Git Bash/CMD)
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

**4. Install Dependencies:**

```bash
pip install -r requirements.txt
```

**5. Configure Environment Variables:**

- Create a file named `.env` in the project root directory.
- Add the following variables, replacing the placeholder values with your actual credentials:

  ```dotenv
  # API Keys
  GOOGLE_API_KEY="YOUR_GOOGLE_AI_API_KEY"
  GROQ_API_KEY="YOUR_GROQ_API_KEY"

  # PostgreSQL Database Credentials
  POSTGRES_DB="your_database_name"
  POSTGRES_USER="your_database_user"
  POSTGRES_PASSWORD="your_database_password"
  POSTGRES_HOST="localhost" # or your DB host
  POSTGRES_PORT="5432"      # or your DB port

  # Google Cloud Configuration (for Imagen)
  GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
  GOOGLE_CLOUD_LOCATION="your-gcp-region" # e.g., us-central1
  ```

**6. Set up Google Cloud Authentication (for Imagen):**

- Run the following command in your activated terminal:
  ```bash
  gcloud auth application-default login
  ```
- Follow the instructions in your browser to log in with the Google account associated with your `GOOGLE_CLOUD_PROJECT`.

**7. Initialize the Database:**

- Make sure your PostgreSQL server is running.
- Run the database initialization script:
  ```bash
  python database.py
  ```
  This will create the necessary tables (`conversations`, `messages`) if they don't exist.

**8. Run the Streamlit Application:**

```bash
streamlit run app.py
```

## Usage

1.  **Open the App:** Access the Streamlit app in your web browser (usually at `http://localhost:8501`).
2.  **Navigate:** Use the sidebar to switch between the "Chat" and "Image Generation" pages.
3.  **Chat Page:**
    - **Select Model:** Choose an LLM from the "Settings" section in the sidebar.
    - **Manage Conversations:** Use the "Conversations" section in the sidebar to start a new chat, select an existing one, or delete conversations.
    - **Interact:** Type your message in the chat input box at the bottom and press Enter.
4.  **Image Generation Page:**
    - Enter a description of the image you want to generate.
    - Select the number of images and the desired style.
    - Click "Generate Images". The generated images will appear below the form.
    - Generation history is stored temporarily for the session.

## Troubleshooting

- **API Key Errors:** Ensure your API keys in the `.env` file are correct and have the necessary permissions.
- **Database Connection Errors:** Verify your PostgreSQL server is running and the credentials in `.env` are accurate.
- **`gcloud` Authentication Errors (Imagen):** Make sure you have run `gcloud auth application-default login` successfully and are logged in with the correct Google account. Ensure the Vertex AI API is enabled for your project.
- **Groq `UnicodeEncodeError`:** If you encounter this error specifically when using Groq models, it might be related to system locale settings interacting with the `httpx` library used by `groq`. This issue is best reported to the `groq-python` library maintainers on GitHub. As a workaround, use Gemini models.
- **Missing Libraries:** Ensure all dependencies are installed using `pip install -r requirements.txt` within your activated virtual environment.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details (you may need to create this file).
