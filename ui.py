import streamlit as st
from chatbot import Chatbot

# -------------------
# Init
# -------------------
if "bot" not in st.session_state:
    st.session_state.bot = Chatbot()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Kotha - AI Chatbot", layout="wide")

# -------------------
# Sidebar (chat history)
# -------------------
with st.sidebar:
    st.title("💬 Chat History")
    if st.session_state.chat_history:
        for i, (q, a) in enumerate(st.session_state.chat_history):
            st.markdown(f"**🧑 You:** {q}")
            st.markdown(f"**🤖 AI:** {a}")
            st.markdown("---")
    else:
        st.info("No conversations yet.")

    if st.button("🗑 Clear History"):
        st.session_state.chat_history = []
        st.rerun()

# -------------------
# Chat area
# -------------------
st.title("🤖 Kotha - Your AI Assistant")

chat_container = st.container()
with chat_container:
    for question, answer in st.session_state.chat_history:
        st.markdown(f"**🧑 You:** {question}")
        st.markdown(f"**🤖 Assistant:** {answer}")
        st.markdown("---")

# -------------------
# Bottom bar (like ChatGPT)
# -------------------
st.markdown(
    """
    <style>
    .chat-input-container {
        display: flex;
        align-items: center;
        gap: 10px;
        position: fixed;
        bottom: 20px;
        left: 20px;
        right: 20px;
        background: white;
        padding: 10px;
        border-radius: 12px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.15);
    }
    .chat-input {
        flex: 1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.container():
    col1, col2, col3 = st.columns([1, 8, 1])

    with col1:
        uploaded_file = st.file_uploader("➕", type=["pdf", "txt", "docx"], label_visibility="collapsed")

    with col2:
        user_input = st.text_input("Type your message...", key="user_input", label_visibility="collapsed")

    with col3:
        send_button = st.button("📤", use_container_width=True)

# -------------------
# Logic
# -------------------
if send_button and user_input:
    response = st.session_state.bot.get_response(user_input)
    st.session_state.chat_history.append((user_input, response))
    st.rerun()

if uploaded_file:
    file_path = f"data/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded: {uploaded_file.name}")
