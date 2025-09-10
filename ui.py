import streamlit as st
from chatbot import Chatbot

# ---------------------------
# Initialize chatbot
# ---------------------------
if "bot" not in st.session_state:
    st.session_state.bot = Chatbot()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Kotha - AI Chatbot", layout="wide")
st.title("🤖 Kotha - Your AI Assistant")

# ---------------------------
# Multi-file uploader
# ---------------------------
uploaded_files = st.file_uploader(
    "📂 Upload PDFs, TXTs, or DOCXs",
    type=["pdf", "txt", "docx"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = f"data/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Add file to KB
        st.session_state.bot.kb.load_document(file_path)
        st.success(f"✅ Loaded and indexed: {uploaded_file.name}")

# ---------------------------
# Chat input
# ---------------------------
user_input = st.chat_input("Ask me something...")

if user_input:
    response, sources = st.session_state.bot.get_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Assistant", response))

    # Show assistant reply
    st.markdown(f"**🤖 Assistant:** {response}")

    # Show sources
    if sources:
        with st.expander("📄 Sources used for this answer"):
            for i, src in enumerate(sources, 1):
                st.markdown(f"**Source {i}:** {src[:500]}...")

# ---------------------------
# Display chat history
# ---------------------------
st.subheader("💬 Conversation History")
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 {role}:** {msg}")
    else:
        st.markdown(f"**🤖 {role}:** {msg}")
