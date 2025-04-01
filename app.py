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
# Import message types for chat history
from langchain_core.messages import HumanMessage, AIMessage
# Import NEW image generation functions for Imagen
from image_generation import (
    setup_image_generator, 
    generate_images_with_imagen, 
    process_imagen_response
)

# --- Available Models ---
AVAILABLE_MODELS = [
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-2.5-pro-exp-03-25",
    "llama3-8b-8192",   # Groq Llama3 8B
    "llama3-70b-8192",  # Groq Llama3 70B
]

# --- Page Selection ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Chat"

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("Navigation")
    page = st.radio("Go to", ["Chat", "Image Generation"])
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
    st.title("🤖 AI Agent Chat")
    st.caption("Your personal AI assistant with conversation history and multi-provider model selection.")

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
        st.header("Settings")
        selected_model = st.selectbox(
            "Choose AI Model",
            options=AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(st.session_state.selected_model),
            key="model_selector"
        )

        if selected_model != st.session_state.selected_model:
            st.session_state.selected_model = selected_model
            st.rerun()

        st.divider()
        st.header("Conversations")

        # Button to create a new conversation
        if st.button("➕ New Conversation"):
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

        st.divider()

        # Refresh and display list of conversations
        if not st.session_state.conversations_list:
            refresh_conversations()

        if not st.session_state.conversations_list:
            st.write("No conversations yet.")
        else:
            # Display conversations as clickable buttons/elements
            for conv in st.session_state.conversations_list:
                conv_id = conv["id"]
                # Use the name from DB directly, it should have the desired format now
                conv_name = conv["name"]
                # Use columns for layout: button and delete icon
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                     if st.button(conv_name, key=f"conv_{conv_id}", use_container_width=True,
                                  type=("primary" if conv_id == st.session_state.current_conversation_id else "secondary")):
                        st.session_state.current_conversation_id = conv_id
                        # Load messages for the selected conversation
                        st.session_state.messages = get_messages(conv_id)
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"del_{conv_id}", help="Delete conversation"):
                        deleted = delete_conversation(conv_id)
                        if deleted:
                            # If deleting the current conversation, reset selection
                            if conv_id == st.session_state.current_conversation_id:
                                st.session_state.current_conversation_id = None
                                st.session_state.messages = []
                            refresh_conversations()
                            st.rerun()
                        else:
                            st.error(f"Failed to delete conversation {conv_id}")

        # Attempt to select the latest conversation if none is selected
        if st.session_state.current_conversation_id is None and st.session_state.conversations_list:
            st.session_state.current_conversation_id = st.session_state.conversations_list[0]["id"]
            st.session_state.messages = get_messages(st.session_state.current_conversation_id)
            # No rerun here to avoid loop if message loading fails

    # --- Get the agent executor based on the selected model ---
    # This call now depends on the selected model from the sidebar
    agent_executor = setup_agent(st.session_state.selected_model)

    # --- Main Chat Area ---

    # Display chat messages based on the selected conversation
    if st.session_state.current_conversation_id:
        # Reload messages if they are empty for the current conv (e.g., after creation)
        if not st.session_state.messages:
             st.session_state.messages = get_messages(st.session_state.current_conversation_id)

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        st.info("Select a conversation or start a new one from the sidebar.")

    # Accept user input
    if prompt := st.chat_input("What do you want to ask the agent?"):
        if not st.session_state.current_conversation_id:
            st.error("Please select or start a new conversation first!")
        # Check if agent executor was successfully created for the selected model
        elif not agent_executor:
            st.error(f"Agent could not be initialized for model '{st.session_state.selected_model}'. Please check the logs.")
        else:
            # Add user message to DB and display immediately
            add_message(st.session_state.current_conversation_id, "user", prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get agent response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Prepare chat history for the agent prompt
                        # Use messages stored in session state, excluding the latest user prompt
                        # which is passed separately via 'input'
                        chat_history_for_prompt = []
                        raw_messages_for_history = st.session_state.messages[:-1]
                        for msg in raw_messages_for_history:
                            if msg["role"] == "user":
                                chat_history_for_prompt.append(HumanMessage(content=msg["content"]))
                            elif msg["role"] == "assistant":
                                chat_history_for_prompt.append(AIMessage(content=msg["content"]))

                        # Invoke the agent with input and formatted chat history
                        response = agent_executor.invoke({
                            "input": prompt,
                            "chat_history": chat_history_for_prompt
                        })
                        response_content = response.get('output', 'Sorry, I had trouble processing that.')

                    except Exception as e:
                        response_content = f"An error occurred during agent processing: {e}"
                        # Log the full traceback for detailed debugging
                        logging.exception("Error during agent invocation:")

                    # Add agent response to DB and display
                    add_message(st.session_state.current_conversation_id, "assistant", response_content)
                    st.markdown(response_content)
                    # Append agent response to session state as well for consistency
                    st.session_state.messages.append({"role": "assistant", "content": response_content})
                    # Optional: Could reload all messages from DB here for ultimate consistency,
                    # but appending is faster for UI responsiveness.
                    # st.session_state.messages = get_messages(st.session_state.current_conversation_id)
                    # st.rerun() 
else:
    # --- Image Generation Interface (Now using Imagen via AI Platform) ---
    st.title("🎨 AI Image Generator (Imagen)")
    st.caption("Generate images using Google Cloud's Imagen model.")

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
        # Image generation form
        with st.form("image_generation_form"):
            prompt = st.text_area(
                "Describe the image you want to generate",
                placeholder="A photorealistic cat wearing sunglasses...",
                height=100
            )
            
            # Additional parameters
            col1, col2 = st.columns(2)
            with col1:
                num_images = st.number_input("Number of images to generate", min_value=1, max_value=8, value=1) # Imagen allows up to 8
            with col2:
                style = st.selectbox(
                    "Image Style (influences prompt)",
                    ["Realistic", "Photographic", "Artistic", "Cartoon", "Abstract", "Watercolor", "Oil Painting"]
                )
            
            submitted = st.form_submit_button("Generate Images")

        if submitted and prompt:
            with st.spinner("Generating images with Imagen..."):
                try:
                    # Call the new Imagen generation function
                    api_response = generate_images_with_imagen(
                        prompt=prompt, 
                        num_images=num_images, 
                        style=style
                    )
                    
                    # Process the response using the new Imagen processing function
                    if api_response:
                        processed_images = process_imagen_response(api_response)
                    else:
                        processed_images = None # API call failed before processing
                    
                    if processed_images:
                        # Add to history
                        st.session_state.image_history.append({
                            "prompt": prompt,
                            "style": style,
                            "timestamp": "Now" # Consider using datetime
                        })
                        
                        # Display the generated images
                        st.success(f"{len(processed_images)} image(s) generated successfully with Imagen!")
                        
                        # Display images in a grid
                        cols = st.columns(len(processed_images)) # Display all generated images
                        for idx, (col, img) in enumerate(zip(cols, processed_images)):
                            with col:
                                st.image(img, caption=f"Generated Image {idx + 1}")
                    else:
                        # Error message displayed by generate_images_with_imagen or process_imagen_response
                        st.warning("Failed to generate or process images. Check the logs for details.") 
                        # No need for extra error here as functions already log/st.error
                
                except Exception as e:
                    # Catch any unexpected error during the Streamlit flow
                    st.error(f"An unexpected error occurred in the application: {e}")
                    logging.exception("Unexpected error in Streamlit image generation flow:")

        # Display image generation history
        if st.session_state.image_history:
            st.divider()
            st.subheader("Generation History")
            
            for entry in reversed(st.session_state.image_history):
                with st.expander(f"Prompt: {entry['prompt']} ({entry['style']})"):
                    st.write(f"Generated at: {entry['timestamp']}")
                    # You could add more details here if needed 