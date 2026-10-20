import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

print(api_key)

# Put your Gemini API key here
API_KEY= os.getenv("API_KEY")

client = genai.Client(api_key=API_KEY)

st.title("🤖 My AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                history = [
                    {
                        "role": "user" if m["role"] == "user" else "model",
                        "parts": [{"text": m["content"]}]
                    }
                    for m in st.session_state.messages
                ]

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=history
                )

                answer = response.text
                st.write(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

    except Exception as e:
        st.error(f"Error: {e}")