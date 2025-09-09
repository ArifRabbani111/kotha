from chatbot import Chatbot

def main():
    bot = Chatbot()
    print("Hello! I'm your AI assistant. Type 'exit' to quit, or 'upload <file>' to add a PDF.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Handle PDF upload
        if user_input.startswith("upload "):
            pdf_path = user_input.split(" ", 1)[1]
            try:
                bot.kb.add_pdf(pdf_path)
                print(f"Assistant: ✅ PDF '{pdf_path}' uploaded successfully.")
            except Exception as e:
                print(f"Assistant: ❌ Error: {e}")
            continue

        # Normal chat
        bot.stream_response(user_input)

if __name__ == "__main__":
    main()

