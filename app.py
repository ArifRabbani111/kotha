import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage

# Load API key from .env file
load_dotenv()

# Check if the API key is loaded
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")

# 1. Define the LLM model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# 2. Set up the chat history
chat_history = []

# 3. Define the prompt template
# This is a key step for "prompt engineering"
# The system message gives the model its "role"
# The 'chat_history' and 'user_question' placeholders will be filled dynamically
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly and helpful assistant. Keep your answers concise and conversational."),
    ("placeholder", "{chat_history}"),
    ("human", "{user_question}")
])

# 4. Create the main conversation loop
def get_llm_response(user_question):
    global chat_history

    # Combine the system message, chat history, and new user question
    # This is how the model "remembers" the conversation
    formatted_prompt = prompt.format_messages(
        chat_history=chat_history,
        user_question=user_question
    )

    # Invoke the LLM with the formatted prompt
    ai_response = model.invoke(formatted_prompt)

    # Update the chat history with both the user's message and the bot's response
    chat_history.append(HumanMessage(content=user_question))
    chat_history.append(AIMessage(content=ai_response.content))

    return ai_response.content

# 5. Run the chatbot
print("Hello! I'm your AI assistant. Type 'exit' to end the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    response = get_llm_response(user_input)
    print(f"Assistant: {response}")