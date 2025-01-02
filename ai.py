from openai import OpenAI
import tkinter as tk

# Initialize an empty list to store conversation history
conversation_history = [{"role": "assistant", "content": "You are a helpful assistant. Always provide concise and accurate answers. Respond in a professional and friendly tone. Most of the time, I will be asking you a  question, usually related to Unix, Linux, Operating Systems, or something of that nature. I will provide 4 possible answers most of the time. Unless I tell you otherwise, only one option is possible, so choose the best one. If you are encountering errors in your logic, please say it, do not just take a best guess. When you send a respose, send your choosing of my option list first, then a newline, and then nothing else. "}]

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
