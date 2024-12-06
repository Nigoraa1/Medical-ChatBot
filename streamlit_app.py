import openai
import streamlit as st
from PIL import Image
import base64

# Step 1: API Key Entry
if "api_key" not in st.session_state or st.session_state.api_key is None:
    st.markdown("### 💉 Welcome to the Medical ChatBot")
    
    # Display an image on top of the app
    image_path = "pic.jpg"  # Replace with your image path
    try:
        image = Image.open(image_path)
        st.image(image, caption="Medical ChatBot", use_column_width=True)
    except FileNotFoundError:
        st.warning("Image file not found. Please check the path.")

    # API Key input
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    if st.button("Submit API Key"):
        if api_key.strip():
            st.session_state.api_key = api_key
            st.success("API Key saved successfully!")
        else:
            st.warning("Please provide a valid API key.")
else:
    # Step 2: Chat Interface
    openai.api_key = st.session_state.api_key

    # Adding a background image
    background_image_path = "m.jpg"  # Replace with your background image path
    try:
        with open(background_image_path, "rb") as bg_image:
            encoded_bg_image = base64.b64encode(bg_image.read()).decode()
        background_css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_bg_image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .user-message {{
            background-color: #007bff;
            color: white;
            padding: 10px;
            border-radius: 10px;
            max-width: 60%;
            margin: 5px 0;
            align-self: flex-end;
        }}
        .assistant-message {{
            background-color: #e8f5e9;
            color: #000;
            padding: 10px;
            border-radius: 10px;
            max-width: 60%;
            margin: 5px 0;
            align-self: flex-start;
        }}
        .message-container {{
            display: flex;
            flex-direction: column;
        }}
        </style>
        """
        st.markdown(background_css, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Background image file not found. Please check the path.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Define the chat agent class
    class MedicalChatAgent:
        def __init__(self):
            self.system_message = """
            
            You are designed to provide information on general medical topics.
            You cannot provide professional medical advice, diagnosis, or treatment, but you can offer general, educational, and reliable information.
            Always recommend consulting a healthcare professional for specific concerns.
            Always be polite and provide clear, helpful responses.
            If asked about other topics, say, "I am specialized only in medical topics."
            Understand greetings and farewells, and respond accordingly.
            """
            self.messages = [{"role": "system", "content": self.system_message}]

        def add_message(self, role, content):
            """Add a message to the conversation history."""
            self.messages.append({"role": role, "content": content})

        def get_response(self, prompt):
            """Generate a response based on the conversation history."""
            self.add_message("user", prompt)
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",  # Use GPT-4 model for better performance
                    messages=self.messages,
                    max_tokens=600,  # Adjust token limit based on the desired response length
                    temperature=0.6,  # Set creativity level for responses
                )
                assistant_reply = response.choices[0].message["content"]
                self.add_message("assistant", assistant_reply)
                return assistant_reply
            except Exception as e:
                st.error(f"Error communicating with OpenAI API: {e}")
                return "I'm sorry, but I couldn't process your request at this time."

    # Create the chat agent instance
    agent = MedicalChatAgent()

    # Display chat messages from history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

    # React to user input
    if prompt := st.chat_input("Ask a medical question:"):
        # Display user message
        st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate and display assistant response
        response = agent.get_response(prompt)
        st.markdown(f'<div class="assistant-message">{response}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
