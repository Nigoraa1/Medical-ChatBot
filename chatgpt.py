import streamlit as st
from datetime import datetime

# Strimlit ilovasini sozlash
st.set_page_config(page_title="Medical ChatBot", page_icon="💉", layout="wide")

# Stil sozlamalari
st.markdown(
    """
    <style>
    .main {
        background-color: #ffe6f2;
    }
    .chat-header {
        color: white;
        background-color: #ff3366;
        padding: 20px;
        text-align: center;
        font-size: 24px;
        border-radius: 10px;
        font-weight: bold;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .chat-container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
        border-radius: 10px;
        background-color: #fff5fa;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    .chat-box {
        background-color: #ffe6f2;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    .chat-input {
        border: 2px solid #ff3366;
        border-radius: 10px;
        padding: 10px;
        width: 100%;
        margin-bottom: 10px;
        font-size: 16px;
    }
    .send-button {
        background-color: #ff3366;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 10px;
        cursor: pointer;
        font-size: 16px;
    }
    .send-button:hover {
        background-color: #cc004c;
    }
    .message-user {
        text-align: right;
        color: #ff3366;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .message-bot {
        text-align: left;
        color: #333;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<div class="chat-header">💉 Medical ChatBot</div>', unsafe_allow_html=True)

# ChatBot logikasi
chat_history = []
def chatbot_response(user_input):
    """Oddiy javob generatori."""
    responses = {
        "salom": "Assalomu alaykum! Sizga qanday yordam bera olaman?",
        "qandli diabet": "Qandli diabet - bu qon shakar miqdorini nazorat qilishni talab qiluvchi kasallikdir. Yordam kerakmi?",
        "bosh og'rig'i": "Bosh og'rig'i sababli dam olish yoki suv ichishni sinab ko'ring. Agar davom etsa, shifokorga murojaat qiling.",
        "rahmat": "Marhamat! Yana savolingiz bo'lsa, so'rang."
    }
    default_response = "Uzr, savolingizni tushunmadim. Iltimos, aniqroq so'rang."
    return responses.get(user_input.lower(), default_response)

# Chat interfeysi
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
def render_chat():
    for message in chat_history:
        if message["sender"] == "user":
            st.markdown(f"<div class='message-user'>Siz: {message['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='message-bot'><b>ChatBot:</b> {message['text']}</div>", unsafe_allow_html=True)

# Foydalanuvchi kirishi
with st.form("chat_form"):
    user_input = st.text_input("Savolingizni kiriting", key="chat_input", placeholder="Masalan: bosh og'rig'i", help="Savolingizni kiriting va yuboring.",
                               label_visibility="collapsed", class_name="chat-input")
    submitted = st.form_submit_button("Yuborish", use_container_width=True, class_name="send-button")

    if submitted and user_input.strip():
        chat_history.append({"sender": "user", "text": user_input})
        response = chatbot_response(user_input)
        chat_history.append({"sender": "bot", "text": response})

# Chatni qayta chizish
render_chat()
st.markdown('</div>', unsafe_allow_html=True)

# Eslatma
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #ff3366;'>© 2024 Medical ChatBot</div>",
    unsafe_allow_html=True
)
