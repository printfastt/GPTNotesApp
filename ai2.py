from openai import OpenAI
import tkinter as tk

# Initialize conversation history with a system message
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant. Always provide concise and accurate answers. Respond in a professional and friendly tone. Most of the time, I will be asking you a  question, usually related to Unix, Linux, Operating Systems, or something of that nature. I will provide 4 possible answers most of the time. Unless I tell you otherwise, only one option is possible, so choose the best one. If you are encountering errors in your logic, please say it, do not just take a best guess."}
]

API_KEY = "NULL"
def ask_chatgpt(user_question=None):
    global conversation_history

    # Initialize OpenAI client
    client = OpenAI(api_key=API_KEY)

    # Append user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_question})

    # Create a chat completion request with the entire conversation history
    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation_history,
        stream=False,  # Stream is set to False for testing, can be set to True later
    )

    # Get the assistant's response
    response_text = response.choices[0].message['content']

    # Append the assistant's response to the conversation history
    conversation_history.append({"role": "assistant", "content": response_text})

    print(response_text)
    return response_text

