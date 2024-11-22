# RUN WITH:
# streamlit run llm_sml.py --server.address 127.0.0.1

import streamlit as st
from streamlit_chat import message
import time
import requests

# Flask API URL
FLASK_API_URL = 'http://127.0.0.1:5000/process_llm'  # Local URL, adjust if hosted differently

# Page Configuration
st.set_page_config(
    page_title="Chimera LLM",
    layout="centered",
)

# Title
st.title("Chimera LLM Chat")

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input handler function
def handle_message():
    query = st.session_state["user_input"]
    if query.strip():
        # Add the user's message to the session state
        st.session_state.messages.append({"role": "user", "content": query})

        # Send the user input to the Flask backend via POST request
        try:
            response = requests.post(FLASK_API_URL, json={"query": query})
            response_json = response.json()
            bot_response = response_json.get("response", "Sorry, I couldn't process that.")

        except requests.exceptions.RequestException as e:
            bot_response = "Error: Unable to connect to the backend."

        # Add the bot's response to the session state
        st.session_state.messages.append({"role": "bot", "content": bot_response})

        # Clear the input field
        st.session_state["user_input"] = ""

# Chat Input Section
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""  # Initialize input field in session state

st.text_area(
    "Your question:",
    value=st.session_state["user_input"],
    placeholder="Ask me anything...",
    height= 70,
    key="user_input",
    on_change=handle_message  # Trigger when Enter is pressed
)


# Display Chat History (Newest on Top)
st.subheader("💬 Chat History")
for i, msg in enumerate(reversed(st.session_state.messages)):  # Reverse the message list
    if msg["role"] == "user":
        # Use custom user avatar image
        user_avatar = "images/user_avatar.png"  # Replace with your custom image file or URL
        # avatar_img = user_avatar
        message(msg["content"], is_user=True, key=f"user-{len(st.session_state.messages) - i}")
    else:
        # Use custom bot avatar image
        bot_avatar = "images/bot_avatar.png"  # Replace with your custom image file or URL
        # avatar_img = bot_avatar
        message(msg["content"], key=f"bot-{len(st.session_state.messages) - i}")















