import streamlit as st
import requests
import json

# OpenRouter API configuration
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = st.text_input("Enter your OpenRouter API Key", type="password")

# Function to get response from DeepSeek R1
def get_deepseek_response(user_input):
    if not API_KEY:
        return "Please enter a valid API key."
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Streamlit app layout
st.title("DeepSeek R1 Chatbot Demo")
st.write("Interact with DeepSeek R1 for free using OpenRouter API")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get and display AI response
    with st.chat_message("assistant"):
        response = get_deepseek_response(user_input)
        st.markdown(response)
    
    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": response})