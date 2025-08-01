
import streamlit as st
from config.settings import settings
from llm_manager.llm_service import LLMManager

# Instantiate LLMManager once (best practice)
llm_manager = LLMManager()

# --- Page Configuration ---
st.set_page_config(
    page_title="Clinic Patient Intake & Pre-Screening Assistant",
    page_icon="🩺",
    layout="wide"
)

# --- Sidebar for Settings Display ---
# with st.sidebar:
#     st.title("LLM Configuration")
#     st.write(f"**Provider:** `{settings.LLM_PROVIDER}`")
#     st.write(f"**Model:** `{settings.LLM_MODEL}`")
#     st.write(f"**Max Tokens:** `{settings.MAX_TOKENS}`")
#     st.write(f"**Temperature:** `{settings.TEMPERATURE}`")
#     st.info("Configuration is loaded from the environment file.")

# --- Title and Header ---
st.title("🩺 Clinic Patient Intake & Pre-Screening Assistant")

# --- Session State for Chat History ---
# if "messages" not in st.session_state:
#     st.session_state.messages = []

if "messages" not in st.session_state:
    # Start with a blank user message
    st.session_state.messages = [{"role": "user", "content": ""}]
    # Generate the first assistant response
    response = llm_manager.get_response(st.session_state.messages, "")
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- Display Chat Messages from History ---
for message in st.session_state.messages:
    # Skip blank user messages
    if message["role"] == "user" and message["content"].strip() == "":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Main Chat Interface ---

hide_input = False
if st.session_state.messages:
    last_msg = st.session_state.messages[-1]
    if last_msg["role"] == "assistant" and "I’ll end our conversation here. Take care." in last_msg["content"]:
        hide_input = True

# Get user input
if not hide_input:
    if prompt := st.chat_input("Respond here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                # Instantiate LLMManager and get response
                # This is the single public method call as per our design

                try:
                    response = llm_manager.get_response(st.session_state.messages, prompt)
                    st.markdown(response)
                except Exception as e:
                    st.error(f"Failed to get response: {e}")
                    response = None  # Handle case where an error occurred
            
            if response:
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                if st.session_state.messages:
                    last_msg = st.session_state.messages[-1]
                    if last_msg["role"] == "assistant" and "I’ll end our conversation here. Take care." in last_msg["content"]:
                        hide_input = True