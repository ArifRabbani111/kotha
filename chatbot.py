# chatbot.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage
from memory import Memory
from knowledge import KnowledgeBase

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# initialize model (you can still use Gemini for generation)
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")  # keep as before

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use provided context when possible. If context is absent, answer concisely."),
    ("placeholder", "{chat_history}"),
    ("human", "{user_question}")
])

class Chatbot:
    def __init__(self, kb_api_embedding=None):
        self.memory = Memory()
        # pass api embedding instance to KnowledgeBase if you want API-first
        self.kb = KnowledgeBase(api_embedding=kb_api_embedding)

    def get_response(self, user_question: str):
        """
        Returns: (answer_text, sources_list, error_message_or_None)
        """
        try:
            # 1. Get relevant docs
            docs = self.kb.similarity_search(user_question)
            context_text = "\n\n".join(docs) if docs else ""

            full_question = f"""Use the following context if relevant (if context is insufficient, answer from general knowledge).

Context:
{context_text}

User question: {user_question}
"""
            formatted_prompt = prompt.format_messages(
                chat_history=self.memory.get_history(),
                user_question=full_question
            )

            # 2. Get response from LLM
            ai_response = model.invoke(formatted_prompt)
            answer = ai_response.content if hasattr(ai_response, "content") else str(ai_response)

            # 3. Update memory
            self.memory.add(HumanMessage(content=user_question))
            self.memory.add(AIMessage(content=answer))

            return answer, docs, None

        except Exception as e:
            # Catch any runtime error and return a friendly message
            err_msg = f"Internal error: {str(e)}"
            # Also log in memory
            self.memory.add(HumanMessage(content=user_question))
            self.memory.add(AIMessage(content=err_msg))
            return err_msg, [], err_msg

