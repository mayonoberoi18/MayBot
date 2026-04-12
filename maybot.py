import streamlit as st
from PIL import Image
import os
from datetime import datetime
import wikipedia
import sympy as sp
import random
from openai import OpenAI

wikipedia.set_lang("en")

# ====================== PAGE CONFIG ======================
logo_path = "illuminati.png"
try:
    favicon = Image.open(logo_path)
except:
    favicon = "🤖"

st.set_page_config(page_title="MayBot", page_icon=favicon, layout="wide")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: #020617;
        background-image: radial-gradient(circle at 25% 25%, rgba(16, 185, 129, 0.18) 0%, transparent 50%),
                          radial-gradient(circle at 75% 75%, rgba(59, 130, 246, 0.18) 0%, transparent 50%);
    }
    .stChatMessage { border-radius: 22px; box-shadow: 0 12px 45px rgba(0,0,0,0.7); padding: 18px 24px; border: 1px solid rgba(255,255,255,0.1); }
    .main-title {
        font-size: 4rem; font-weight: 900;
        background: linear-gradient(90deg, #10b981, #3b82f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def load_logo():
    return Image.open(logo_path) if os.path.exists(logo_path) else None

logo_img = load_logo()

# ====================== CONFIG ======================
st.sidebar.header("🔧 MayBot Settings")

api_key = st.sidebar.text_input("OpenAI / Grok API Key", type="password", value=st.session_state.get("api_key", ""))
if api_key:
    st.session_state.api_key = api_key

# Choose model (Grok or GPT)
model_choice = st.sidebar.selectbox(
    "Choose AI Model",
    ["grok-beta", "gpt-4o-mini", "gpt-4o"],
    index=0
)

client = OpenAI(
    api_key=st.session_state.get("api_key"),
    base_url="https://api.x.ai/v1" if "grok" in model_choice.lower() else None
) if st.session_state.get("api_key") else None

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm MayBot 😊 Created by Mayon Oberoi from Nagpur. How can I help you today?"}]

# ====================== RESPONSE WITH REAL LLM ======================
def get_vast_answer(user_query):
    if not client:
        return "Please enter your API key in the sidebar to unlock full intelligence! 💡"

    try:
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        messages.append({"role": "user", "content": user_query})

        response = client.chat.completions.create(
            model=model_choice,
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Oops! Error: {str(e)}\n\nMake sure your API key is correct."

# ====================== SIDEBAR ======================
with st.sidebar:
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hello again! 😊 What would you like to talk about?"}]
        st.rerun()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm MayBot 😊 How can I help you today?"}]
        st.rerun()

    st.divider()
    st.caption("Powered by Mayon Oberoi • Nagpur, India 🇮🇳")

# ====================== HEADER ======================
if logo_img:
    st.image(logo_img, width=140)
st.markdown('<h1 class="main-title">MayBot</h1>', unsafe_allow_html=True)
st.caption("Your Intelligent Voice-Enabled Companion")

# ====================== VOICE INPUT ======================
st.markdown("### 🎤 Voice Input")

col1, col2 = st.columns([1, 4])

with col1:
    if st.button("🎤 Speak Now", type="primary", use_container_width=True):
        voice_html = """
        <script>
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                window.location.search = "?voice=" + encodeURIComponent(transcript);
            };
            recognition.onerror = function(e) { alert("Voice error: " + e.error); };
            recognition.start();
        </script>
        """
        st.components.v1.html(voice_html, height=0)

with col2:
    audio_file = st.audio_input("Or record voice message (Whisper will transcribe)")

# Handle browser voice
if "voice" in st.query_params:
    transcript = st.query_params["voice"]
    if transcript:
        st.session_state.messages.append({"role": "user", "content": transcript})
        st.rerun()

# Handle Whisper transcription (better accuracy)
if audio_file and client:
    with st.spinner("Transcribing with Whisper..."):
        try:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            ).text
            st.success(f"Transcribed: {transcript[:100]}...")
            st.session_state.messages.append({"role": "user", "content": transcript})
            st.rerun()
        except:
            st.error("Transcription failed. Check API key.")

# ====================== CHAT DISPLAY ======================
for i, msg in enumerate(st.session_state.messages):
    avatar = logo_img if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
        
        # Add "Read Aloud" button for assistant messages
        if msg["role"] == "assistant" and i > 0:
            if st.button("🔊 Read Aloud", key=f"read_{i}"):
                tts_html = f"""
                <script>
                    const utterance = new SpeechSynthesisUtterance(`{msg['content'].replace('`', '')}`);
                    utterance.rate = 1.0;
                    utterance.pitch = 1.1;
                    speechSynthesis.speak(utterance);
                </script>
                """
                st.components.v1.html(tts_html, height=0)

# ====================== CHAT INPUT ======================
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=logo_img):
        with st.spinner("Thinking..."):
            response = get_vast_answer(prompt)
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
