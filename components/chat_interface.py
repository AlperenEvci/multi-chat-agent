import streamlit as st
from config.constants import SESSION_KEYS
from database import get_messages, add_message
from langchain_core.messages import HumanMessage, AIMessage
import logging

def render_chat_interface(agent_executor):
    """Render the chat interface."""
    # Header
    st.markdown("""
        <div class="header">
            <h2 style="color: #2196f3;">💬 AI Chat</h2>
            <p style="color: #666;">Ask anything to your AI assistant</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    display_chat_messages()
    
    # Chat input
    handle_chat_input(agent_executor)

def display_chat_messages():
    """Display the chat messages."""
    if st.session_state.get(SESSION_KEYS["current_conversation_id"]):
        if not st.session_state.get(SESSION_KEYS["messages"]):
            st.session_state[SESSION_KEYS["messages"]] = get_messages(
                st.session_state[SESSION_KEYS["current_conversation_id"]]
            )
        
        for message in st.session_state.get(SESSION_KEYS["messages"], []):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        st.info("Select a conversation or start a new one from the sidebar.")

def handle_chat_input(agent_executor):
    """Handle user input and generate AI responses."""
    if prompt := st.chat_input("What do you want to ask the agent?"):
        if not st.session_state.get(SESSION_KEYS["current_conversation_id"]):
            st.error("Please select or start a new conversation first!")
        elif not agent_executor:
            st.error(f"Agent could not be initialized for model '{st.session_state.get(SESSION_KEYS['selected_model'])}'. Please check the logs.")
        else:
            # Add user message to DB and display immediately
            add_message(
                st.session_state[SESSION_KEYS["current_conversation_id"]],
                "user",
                prompt
            )
            st.session_state[SESSION_KEYS["messages"]].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get agent response with loading animation
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    try:
                        chat_history_for_prompt = []
                        raw_messages_for_history = st.session_state[SESSION_KEYS["messages"]][:-1]
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
                    add_message(
                        st.session_state[SESSION_KEYS["current_conversation_id"]],
                        "assistant",
                        response_content
                    )
                    st.markdown(response_content)
                    st.session_state[SESSION_KEYS["messages"]].append(
                        {"role": "assistant", "content": response_content}
                    ) 