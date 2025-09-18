from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

class Chatbot:
    def __init__(self, api_key, knowledge_base=None):
        self.model = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash-lite",
            google_api_key=api_key
        )
        self.knowledge_base = knowledge_base
        self.chat_history = []

    def ask(self, user_input):
        context = ""
        if self.knowledge_base:
            results = self.knowledge_base.retrieve(user_input)
            if results:
                context = "\n".join([doc.page_content for doc in results])

        full_prompt = f"Use the following context if relevant:\n{context}\n\nQuestion: {user_input}"
        response = self.model.invoke([HumanMessage(content=full_prompt)])

        self.chat_history.append(("User", user_input))
        self.chat_history.append(("Bot", response.content))
        return response.content


