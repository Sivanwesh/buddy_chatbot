from google import genai
from google.genai import types


def gemini_chat():
    client = genai.Client(api_key="AQ.Ab8RN6KQhkgMxHXQ_OZOeCwFvNZCis0utka_VNi0XVIGsbcE7g")

    # Define the rules for the AI's behavior
    chat_config = types.GenerateContentConfig(
        system_instruction="Keep all your answers extremely short, concise, and to the point. Use no more than one or two sentences. "
        "You control 180-degree rotatable servomotors. The rest position is [180, 0, 90] for the sequence "
        "[left_hand, right_hand, head], meaning both hands are parallel to the body and the head is straight. "
        "When asked to move a hand or the head, generate the updated array [left_hand, right_hand, head] "
        "corresponding to the instruction. If commanded to move legs, or if commanded to rotate the back, "
        "you must output an error message."
    )

    # Pass the config when creating the chat
    chat = client.chats.create(
        model="gemini-3.6-flash",
        config=chat_config
    )

    print("Chat session started! (Short replies enabled). Type 'quit' to exit.\n")
    print("-" * 50)

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['quit', 'exit']:
            print("Ending chat. Goodbye!")
            break

        response = chat.send_message(user_input)
        print(f"Gemini: {response.text}\n")


if __name__ == "__main__":
    gemini_chat()