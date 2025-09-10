import streamlit as st
from chatbot import Chatbot
from knowledge import load_document


# Initialize chatbot
if "bot" not in st.session_state:
    st.session_state.bot = Chatbot()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Kotha - AI Chatbot", layout="wide")
st.title("🤖 Kotha - Your AI Assistant")

# File uploader
uploaded_file = st.file_uploader("📂 Upload a PDF or TXT", type=["pdf", "txt"])

if uploaded_file is not None:
    file_path = f"data/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    content = load_document(file_path)
    st.success(f"Loaded: {uploaded_file.name} ({len(content)} chars)")
    st.session_state.bot.kb.add_document(content)

# Chat input
user_input = st.chat_input("Ask me something...")

if user_input:
    response = st.session_state.bot.get_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Assistant", response))

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 {role}:** {msg}")
    else:
        st.markdown(f"**🤖 {role}:** {msg}")
