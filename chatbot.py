import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage
from memory import Memory
from knowledge import KnowledgeBase


# Load API key
load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Initialize Gemini model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly and helpful assistant. Keep your answers concise and conversational."),
    ("placeholder", "{chat_history}"),
    ("human", "{user_question}")
])



class Chatbot:
    def __init__(self):
        self.memory = Memory()
        self.kb = KnowledgeBase()

    def get_response(self, user_question):
        # Search knowledge base
        docs = self.kb.similarity_search(user_question, k=3)

        # Step 2: Prepare context for the LLM
        context_text = "\n\n".join(docs)
        full_question = f"""
        Use the following context if relevant. 
        If the context is not enough, answer from your general knowledge.

        Context:
        {context_text}

        User question: {user_question}
        """

        # Step 3: Format prompt with history
        formatted_prompt = prompt.format_messages(
            chat_history=self.memory.get_history(),
            user_question=full_question
        )

       # Step 4: Generate response
        ai_response = model.invoke(formatted_prompt)
        
       # Step 5: Update memory
        self.memory.add(HumanMessage(content=user_question))
        self.memory.add(AIMessage(content=ai_response.content))

       # Step 6: Return response + sources
        return ai_response.content, docs

