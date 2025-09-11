import os
import streamlit as st
from dotenv import load_dotenv
from knowledge import KnowledgeBase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# --- LOAD API KEY ---
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("GOOGLE_API_KEY not found in .env file")
    st.stop()

# --- PAGE CONFIG ---
st.set_page_config(page_title="Kotha AI", page_icon="💬", layout="wide")
st.title("💬 Kotha — Your Personal Knowledge Chatbot")

# --- SESSION STATE INIT ---
if "kb" not in st.session_state:
    st.session_state.kb = KnowledgeBase(API_KEY)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "llm" not in st.session_state:
    st.session_state.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=API_KEY)

# --- SIDEBAR: FILE UPLOAD ---
with st.sidebar:
    st.header("📁 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, or TXT files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if uploaded_files:
        with st.spinner("📚 Processing files..."):
            for file in uploaded_files:
                temp_path = os.path.join("temp_" + file.name)
                with open(temp_path, "wb") as f:
                    f.write(file.read())
                st.session_state.kb.add_file(temp_path)
                os.remove(temp_path)
        st.success("✅ Documents added to knowledge base")

# --- MAIN CHAT ---
user_question = st.chat_input("Ask something from your uploaded documents...")

if user_question:
    if not st.session_state.kb.vector_store:
        st.error("Please upload some documents first.")
    else:
        with st.spinner("🤔 Thinking..."):
            # Retrieve relevant context
            docs = st.session_state.kb.retrieve(user_question, k=3)
            context = "\n\n".join([doc.page_content for doc in docs])

            # Ask LLM to answer using retrieved context
            prompt = f"Use the following context to answer the question accurately:\n\n{context}\n\nQuestion: {user_question}"
            response = st.session_state.llm.invoke([HumanMessage(content=prompt)])
            answer = response.content

        # Save to chat history
        st.session_state.chat_history.append((user_question, answer))

# --- DISPLAY CHAT HISTORY ---
for q, a in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(q)
    with st.chat_message("assistant"):
        st.markdown(a)
