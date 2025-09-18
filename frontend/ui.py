import streamlit as st
import requests

# --- Streamlit Page Config ---
st.set_page_config(page_title="Kotha AI", page_icon="", layout="wide")

# --- Sidebar for file upload ---
with st.sidebar:
    st.title(" Upload Documents")
    st.caption("Add your PDF, TXT, or DOCX files here")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
        help="Upload your documents to chat with them"
    )
    
    if uploaded_files:
        with st.spinner("Processing files..."):
            for file in uploaded_files:
                files = {"file": (file.name, file.getvalue(), "application/octet-stream")}
                try:
                    res = requests.post("http://localhost:5000/upload", files=files, timeout=120)
                    if res.status_code == 200:
                        st.success(f" {file.name}")
                        # Add upload message to chat
                        if "messages" not in st.session_state:
                            st.session_state.messages = []
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": f" **{file.name}** uploaded and processed successfully!"
                        })
                    else:
                        st.error(f" {file.name}: {res.text}")
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": f" Failed to upload **{file.name}**: {res.text}"
                        })
                except Exception as e:
                    st.error(f" {file.name}: {e}")
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f" Error uploading **{file.name}**: {e}"
                    })

# --- Main Chat Area ---
st.title(" Kotha AI")
st.caption("Ask questions about your uploaded documents")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to chat
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:5000/generate",
                    json={"question": prompt},
                    timeout=120
                )
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer returned.")
                else:
                    answer = f"Error: {response.status_code} - {response.text}"
            except Exception as e:
                answer = f"Backend error: {e}"

        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

# --- Clear chat button ---
if st.session_state.messages:
    if st.button(" Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.rerun()
