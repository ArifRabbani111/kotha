import json
import os
from langchain.schema import AIMessage, HumanMessage

HISTORY_FILE = "chat_history.json"

class Memory:
    def __init__(self):
        self.history = []
        self.load()

    def load(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
                for msg in data:
                    if msg["type"] == "human":
                        self.history.append(HumanMessage(content=msg["content"]))
                    else:
                        self.history.append(AIMessage(content=msg["content"]))

    def save(self):
        data = [{"type": "human" if isinstance(m, HumanMessage) else "ai",
                 "content": m.content} for m in self.history]
        with open(HISTORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def add(self, message):
        self.history.append(message)
        self.save()

    def get_history(self):
        return self.history
