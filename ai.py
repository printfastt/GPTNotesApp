from openai import OpenAI
import tkinter as tk

# Initialize an empty list to store conversation history
conversation_history = [{"role": "assistant", "content": "You are a helpful assistant. Always provide concise and accurate answers. Respond in a professional and friendly tone."}]

API_KEY = "NULL"

def ask_chatgpt(user_question=None):
    global conversation_history  # Use the global conversation history

    client = OpenAI(api_key=API_KEY)

    # Append the user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_question})

    # Create a chat completion request with the entire conversation history
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=conversation_history,
        stream=True,
    )

    # Collect and concatenate the response parts
    response = ""
    for part in stream:
        response += part.choices[0].delta.content or ""

    # Append the assistant's response to the conversation history
    conversation_history.append({"role": "assistant", "content": response})

    # Print the full response in a single line
    print(response)
    return response
