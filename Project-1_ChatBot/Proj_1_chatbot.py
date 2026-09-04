import re

GREETING_WORDS = ["hi", "hello", "hey", "hii", "yo"]
EXIT_WORDS = ["bye", "exit", "quit", "goodbye", "see you"]


def contains_word(text, phrase):
    pattern = r"\b" + re.escape(phrase) + r"\b"
    return re.search(pattern, text) is not None


def get_response(user_input):
    text = user_input.lower().strip()

    if any(contains_word(text, word) for word in EXIT_WORDS):
        return "Bot: Goodbye! Have a nice day. \U0001F44B", True

    elif any(contains_word(text, word) for word in GREETING_WORDS):
        return "Bot: Hello there! How can I help you today?", False

    elif "how are you" in text:
        return "Bot: I'm just a program, so I'm always doing fine! How about you?", False

    elif "your name" in text or "who are you" in text:
        return "Bot: I'm ChatBot, a simple rule-based assistant built in Python.", False

    elif "help" in text:
        return ("Bot: You can say hi, ask my name, ask how I am, say thanks, "
                "or type 'bye' to exit."), False

    elif "thank" in text:
        return "Bot: You're welcome! Happy to help.", False

    else:
        # Fallback: nothing matched any known rule.
        return "Bot: Sorry, I didn't understand that. Type 'help' to see what I can do.", False


def main():
    print("=====================================")
    print(" Simple Rule-Based Chatbot")
    print(" Type 'help' for options, 'bye' to quit")
    print("=====================================")

    while True:
        user_input = input("You: ")

        # Basic input validation - ignore empty messages instead of
        # crashing or wasting a turn on the fallback response.
        if user_input.strip() == "":
            print("Bot: Please type something.")
            continue

        response, should_exit = get_response(user_input)
        print(response)

        if should_exit:
            break  # breaks out of the while loop, ending the program


if __name__ == "__main__":
    main()
