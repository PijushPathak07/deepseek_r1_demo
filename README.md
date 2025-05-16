# DeepSeek R1 Chatbot Demo: Solution/Architecture Documentation

## 1. Overview
The DeepSeek R1 Chatbot Demo is a free, web-based AI solution that leverages DeepSeek R1, a powerful reasoning model, to provide interactive chat functionality. The application is built using Python, with Streamlit for the frontend and OpenRouter’s API to access DeepSeek R1 for free. This document details the solution’s architecture, setup process, and usage instructions.

### Objective
Create a demo AI chatbot that:
- Uses DeepSeek R1 for natural language processing and reasoning.
- Is free to set up and use (via OpenRouter’s free tier).
- Provides a simple, user-friendly web interface.
- Handles user queries and displays responses in a conversational format.

## 2. Architecture
The solution follows a client-server architecture with a frontend, backend, and external API integration.

### Components
1. **Frontend (Streamlit)**:
   - A Python-based web framework for creating interactive interfaces.
   - Displays a chat interface with input fields and conversation history.
   - Hosted locally or deployable to Streamlit Community Cloud.
2. **Backend (Python)**:
   - A Python script (`app.py`) that handles API calls and user interactions.
   - Processes user inputs and formats API requests.
   - Manages session state for chat history.
3. **External API (OpenRouter)**:
   - Provides access to DeepSeek R1 via the `/chat/completions` endpoint.
   - Uses the `deepseek/deepseek-r1:free` model for free tier access.
   - Requires an API key for authentication.

### Data Flow
1. **User Input**: The user enters a query in the Streamlit interface.
2. **Frontend Processing**: Streamlit captures the input and sends it to the backend.
3. **Backend API Call**: The Python script constructs a POST request with the user’s query and sends it to OpenRouter’s API.
4. **API Response**: OpenRouter processes the request using DeepSeek R1 and returns a response.
5. **Frontend Display**: The backend parses the response and displays it in the Streamlit chat interface.
6. **Session Management**: The conversation is stored in Streamlit’s session state for continuity.

### Diagram
```
User
   │
   ▼
Streamlit Frontend
   │  ──►  Displays Chat UI
   │  ◄──  Renders Response
   ▼
Python Backend
   │  ──►  Handles API Calls
   │  ◄──  Returns Response
   ▼
OpenRouter API (DeepSeek R1)
   │  ──►  Processes Query
   │  ◄──  Sends Response

```

### Technologies
- **Python 3.8+**: Core programming language.
- **Streamlit**: Web interface framework.
- **Requests Library**: For HTTP requests to OpenRouter.
- **OpenRouter API**: Access to DeepSeek R1 (`deepseek/deepseek-r1:free`).
- **DeepSeek R1**: AI model for reasoning and natural language processing.

## 3. Setup Instructions
Follow these steps to set up the DeepSeek R1 Chatbot Demo locally. The process is free, assuming you use OpenRouter’s free tier.

### Prerequisites
- **Python 3.8 or higher**: Download from [python.org](https://www.python.org/downloads/).
- **OpenRouter Account**: Sign up at [openrouter.ai](https://openrouter.ai) for a free API key.
- **Text Editor**: VS Code, PyCharm, or any editor for Python.
- **Terminal**: Command line interface (e.g., Terminal on macOS/Linux, Command Prompt/PowerShell on Windows).

### Step-by-Step Setup
1. **Create an OpenRouter Account**:
   - Visit [openrouter.ai](https://openrouter.ai) and sign up.
   - Navigate to the API section in your dashboard.
   - Generate a free API key and save it securely.
   - Verify access to the `deepseek/deepseek-r1:free` model in the free tier.

2. **Set Up Project Directory**:
   ```bash
   mkdir deepseek-r1-demo
   cd deepseek-r1-demo
   ```

3. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**:
   ```bash
   pip install streamlit requests
   ```

5. **Create the Application Code**:
   - Create a file named `app.py` in the `deepseek-r1-demo` directory.
   - Copy the following code into `app.py`:

   ```python
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
       if not user_input.strip():
           return "Please enter a valid message."
       
       headers = {
           "Authorization": f"Bearer {API_KEY}",
           "Content-Type": "application/json"
       }
       
       payload = {
           "model": "deepseek/deepseek-r1:free",  # Free tier model
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
           return f"Error: {str(e)}\nResponse: {response.text if 'response' in locals() else 'No response'}"

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
   ```

6. **Run the Application**:
   ```bash
   streamlit run app.py
   ```
   - This starts a local web server, typically at `http://localhost:8501`.
   - Open the URL in a web browser.

7. **Enter API Key**:
   - In the Streamlit interface, input your OpenRouter API key in the provided text box.

### Troubleshooting Setup Issues
- **Python Not Found**: Ensure Python is installed and added to your system’s PATH.
- **Module Not Found**: Verify that `streamlit` and `requests` are installed in the virtual environment (`pip list`).
- **API Key Invalid**: Regenerate the API key in OpenRouter’s dashboard.
- **Port Conflict**: If `localhost:8501` is in use, Streamlit will suggest an alternative port.

## 4. Usage Instructions
Once the application is running, you can interact with the chatbot via the Streamlit web interface.

### How to Use
1. **Access the Interface**:
   - Open `http://localhost:8501` in your browser after running `streamlit run app.py`.
2. **Enter API Key**:
   - Paste your OpenRouter API key into the password field at the top of the page.
3. **Start Chatting**:
   - Type a query in the chat input box (e.g., “What is the theory of relativity?”).
   - Press Enter to submit.
   - The chatbot displays your query and DeepSeek R1’s response in a conversational format.
4. **View Chat History**:
   - Previous messages are shown above the input box, with user messages and AI responses clearly distinguished.
5. **Clear Session**:
   - Refresh the browser to reset the chat history (session state is not persistent across sessions).

### Sample Queries
- **General Knowledge**: “What is the capital of Japan?”
- **Reasoning**: “Why does time slow down near a black hole?”
- **Coding**: “Write a Python function to check if a number is prime.”
- **Debugging**: “Fix this code: [paste buggy code].”

### Expected Behavior
- **Valid Input**: The chatbot responds with accurate, context-aware answers from DeepSeek R1.
- **Empty Input**: Displays “Please enter a valid message.”
- **Invalid API Key**: Displays “Please enter a valid API key.”
- **API Error**: Shows an error message with details (e.g., “Error: 400 Client Error…”).

### Limitations
- **Free Tier Quota**: OpenRouter’s free tier has usage limits (e.g., requests per day). Monitor your dashboard to avoid exceeding limits.
- **Response Time**: Dependent on API latency, typically a few seconds.
- **Session Persistence**: Chat history is lost on browser refresh or app restart.

## 5. Conclusion
The DeepSeek R1 Chatbot Demo is a lightweight, free solution for interacting with an advanced AI model. By using OpenRouter’s free tier and Streamlit’s simplicity, it provides an accessible way to explore DeepSeek R1’s capabilities. Follow the setup and usage instructions to run the demo locally, and consider optional enhancements for a more robust application.
