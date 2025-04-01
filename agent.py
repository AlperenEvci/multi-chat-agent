# agent.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# Import necessary chat model classes
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI # Keep commented out unless needed
# from langchain_anthropic import ChatAnthropic # Keep commented out unless needed
# from langchain_community.chat_models import ChatOllama # Keep commented out unless needed

from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub # Hub for prompt templates
from tools import agent_tools # Import the tools we defined
import logging # Import logging

def create_agent_executor(model_name: str = "gemini-2.5-pro-exp-03-25"):
    """Creates the LangChain agent executor with a specified model from various providers."""
    logging.info(f"Attempting to create agent executor with model: {model_name}")
    # Load environment variables
    load_dotenv()

    # --- 1. Initialize the LLM based on model_name prefix or value ---
    llm = None
    try:
        # Identify provider based on model name (simple prefix check)
        if model_name.startswith("gemini"):
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=0.7,
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
            logging.info(f"Initialized Google Generative AI with model: {model_name}")
        elif model_name.startswith("llama3"):
             # Check if Groq API key exists
             groq_api_key = os.getenv("GROQ_API_KEY")
             if not groq_api_key:
                 raise ValueError("GROQ_API_KEY not found in environment variables.")
             llm = ChatGroq(
                 model_name=model_name,
                 temperature=0.7,
                 groq_api_key=groq_api_key
             )
             logging.info(f"Initialized ChatGroq with model: {model_name}")
        # --- Add other providers here as elif blocks --- 
        # elif model_name.startswith("gpt-"):
        #     openai_api_key = os.getenv("OPENAI_API_KEY")
        #     if not openai_api_key: raise ValueError("OPENAI_API_KEY not found")
        #     llm = ChatOpenAI(model=model_name, temperature=0.7, openai_api_key=openai_api_key)
        #     logging.info(f"Initialized ChatOpenAI with model: {model_name}")
        # elif model_name.startswith("claude"):
        #     anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        #     if not anthropic_api_key: raise ValueError("ANTHROPIC_API_KEY not found")
        #     llm = ChatAnthropic(model=model_name, temperature=0.7, anthropic_api_key=anthropic_api_key)
        #     logging.info(f"Initialized ChatAnthropic with model: {model_name}")
        # elif model_name in ["some-ollama-model"]: # Or check for Ollama connection
        #     llm = ChatOllama(model=model_name, temperature=0.7)
        #     logging.info(f"Initialized ChatOllama with model: {model_name}")
        else:
            raise ValueError(f"Unsupported model provider for: {model_name}")

    except Exception as e:
        logging.error(f"Failed to initialize LLM for model {model_name}: {e}")
        raise # Re-raise the exception to be caught by the caller (e.g., Streamlit app)

    # --- 2. Get the Tools ---
    tools = agent_tools
    # print(f"Tools loaded: {[tool.name for tool in tools]}") # Keep logging concise

    # --- 3. Create the Prompt ---
    # We'll use a standard ReAct chat prompt from Langchain Hub
    # This prompt guides the LLM on how to use tools within a conversation
    try:
        prompt_template = hub.pull("hwchase17/react-chat")
    except Exception as e:
        logging.error(f"Failed to pull prompt template: {e}")
        raise

    # --- 4. Create the Agent ---
    # This binds the LLM, tools, and prompt together
    # The create_react_agent function formats the tools and prompt correctly
    try:
        agent = create_react_agent(llm, tools, prompt_template)
        logging.info("Agent created successfully.")
    except Exception as e:
        logging.error(f"Failed to create react agent: {e}")
        raise

    # --- 5. Create the Agent Executor ---
    # The AgentExecutor runs the agent loop (thought, action, observation)
    try:
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True, # Set to True to see the agent's thought process (VERY useful for debugging)
            handle_parsing_errors=True, # Try to gracefully handle LLM output errors
            max_iterations=5 # Prevent potential infinite loops
        )
        logging.info("Agent Executor created.")
    except Exception as e:
        logging.error(f"Failed to create agent executor: {e}")
        raise

    return agent_executor

if __name__ == '__main__':
    # Updated test block
    models_to_test = ["gemini-1.5-flash", "llama3-8b-8192"] # Add Groq model
    print("--- Running Agent Creation Tests ---")
    for model in models_to_test:
        print(f"Testing with model: {model}...")
        try:
            # Ensure API keys are loaded for the test environment
            load_dotenv()
            # Check if necessary API key exists before testing
            if model.startswith("gemini") and not os.getenv("GOOGLE_API_KEY"):
                print(f"Skipping {model}: GOOGLE_API_KEY not found.")
                continue
            if model.startswith("llama3") and not os.getenv("GROQ_API_KEY"):
                print(f"Skipping {model}: GROQ_API_KEY not found.")
                continue

            executor = create_agent_executor(model_name=model)
            print(f"SUCCESS: Agent Executor created for {model}.")
            # Optional: Add a simple invoke test here if needed
            # response = executor.invoke({"input": "Hello!"})
            # print(f"Response from {model}: {response.get('output','')[:50]}...")
        except Exception as e:
            print(f"FAILED: Error creating agent executor for {model}: {e}")
    print("--- Agent Creation Tests Complete ---")