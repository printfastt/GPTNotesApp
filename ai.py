from openai import OpenAI
import tkinter as tk

conversation_history = [{"role": "assistant", "content": "You are a helpful assistant. Always provide concise and accurate answers. Respond in a professional and friendly tone."}]

API_KEY = "NULL"

def ask_chatgpt(user_question=None):
    global conversation_history  

    client = OpenAI(api_key=API_KEY)

    conversation_history.append({"role": "user", "content": user_question})

    stream = client.chat.completions.create(
        model="gpt-4",
        messages=conversation_history,
        stream=True,
    )

    response = ""
    for part in stream:
        response += part.choices[0].delta.content or ""

    conversation_history.append({"role": "assistant", "content": response})

    print(response)
    return response
