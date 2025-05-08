import streamlit as st
from streamlit_chat import message
import requests
import json
import os
from dotenv import load_dotenv

# Carregar variável de ambiente
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek/deepseek-chat-v3-0324:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Cabeçalhos da API
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Configuração da página
st.set_page_config(page_title="Chat com DeepSeek", page_icon="🤖")
st.title("🤖 Chat com IA (DeepSeek via OpenRouter)")

# Sessão do chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Você é um assistente de IA útil, claro e simpático."}]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mostrar histórico
for i, chat in enumerate(st.session_state.chat_history):
    message(chat["user"], is_user=True, key=f"user_{i}")
    message(chat["ai"], key=f"ai_{i}")

# Entrada do usuário
user_input = st.chat_input("Digite sua mensagem...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Pensando..."):
        response = requests.post(API_URL, headers=HEADERS, data=json.dumps({
            "model": MODEL,
            "messages": st.session_state.messages,
            "temperature": 0.7
        }))

        if response.status_code == 200:
            ai_reply = response.json()["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            st.session_state.chat_history.append({"user": user_input, "ai": ai_reply})
            message(user_input, is_user=True)
            message(ai_reply)
        else:
            st.error(f"Erro na API ({response.status_code})")
            st.code(response.text)
