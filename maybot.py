import streamlit as st
from PIL import Image
import os
from datetime import datetime
import wikipedia
import sympy as sp
import random
import re
import time

wikipedia.set_lang("en")

# Page Config
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
    .main-title { font-size: 4.2rem; font-weight: 900; background: linear-gradient(90deg, #10b981, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
</style>
""", unsafe_allow_html=True)

def load_logo():
    return Image.open(logo_path) if os.path.exists(logo_path) else None

logo_img = load_logo()

# Content
jokes = ["Why don't skeletons fight each other? They don't have the guts! 😂", "Why did the scarecrow win an award? He was outstanding in his field! 🌾"]
fun_facts = ["Octopuses have three hearts!", "Honey never spoils!", "A group of flamingos is called a flamboyance."]
quotes = ["The only way to do great work is to love what you do. – Steve Jobs", "Be the change you wish to see in the world. – Mahatma Gandhi"]

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hey! I'm MayBot 😊 Created by Mayon from Nagpur. How can I help you today?"}]

if "last_topics" not in st.session_state:
    st.session_state.last_topics = []

# Improved Emotion Detection (kept light)
def detect_emotion(text):
    t = text.lower()
    if any(w in t for w in ["sad", "down", "depressed", "upset"]): return "sad"
    if any(w in t for w in ["frustrated", "angry", "annoyed"]): return "frustrated"
    if any(w in t for w in ["anxious", "worried"]): return "anxious"
    if any(w in t for w in ["happy", "great", "excited"]): return "positive"
    return "neutral"

def get_best_response(user_query):
    q = user_query.strip()
    q_lower = q.lower()

    st.session_state.last_topics.append(q_lower)
    if len(st.session_state.last_topics) > 8:
        st.session_state.last_topics.pop(0)

    emotion = detect_emotion(q)

    # === BROADER KNOWLEDGE TRIGGER (This should fix most "not answering" issues) ===
    knowledge_words = ["what", "who", "where", "when", "why", "how", "tell me", "explain", "define", "about", "meaning of", "history of"]
    if any(word in q_lower for word in knowledge_words) and len(q) > 5:
        try:
            # Clean the query
            term = re.sub(r'^(what is|who is|tell me about|explain|what|who|how|why)\s+', '', q, flags=re.I).strip()
            if not term:
                term = q

            titles = wikipedia.search(term, results=3)
            if titles:
                summary = wikipedia.summary(titles[0], sentences=8, auto_suggest=True)
                page = wikipedia.page(titles[0])
                return f"**{page.title}**\n\n{summary.strip()}\n\nSource: {page.url}\n\nAnything else you'd like to know about this?"
        except Exception as e:
            pass  # Fall through to other handlers

    # === Math ===
    if any(c.isdigit() for c in q) or any(op in q_lower for op in ["+", "-", "*", "/", "^", "calculate", "solve", "what is"]):
        try:
            expr = q.replace('^', '**').replace('x', '*').replace('X', '*').replace(' ', '')
            if '=' in expr:
                left, right = expr.split('=', 1)
                result = sp.sympify(f"{left} - ({right})").evalf(12)
            else:
                result = sp.sympify(expr).evalf(12)
            clean = int(result) if result.is_integer else str(result).rstrip('0').rstrip('.')
            return f"The answer is **{clean}**.\n\nWant a step-by-step explanation?"
        except:
            pass

    # === Fun Intents ===
    if re.search(r'\b(joke|funny|laugh)\b', q_lower):
        return random.choice(jokes) + "\n\nWant another one?"
    if re.search(r'\b(fun fact|fact)\b', q_lower):
        return "🌟 Fun Fact: " + random.choice(fun_facts)
    if re.search(r'\b(quote|motivation)\b', q_lower):
        return "💡 " + random.choice(quotes)

    # === Emotional Support ===
    if emotion == "sad":
        return "I'm sorry you're feeling down. It's okay to feel this way. I'm here to listen if you want to talk about it."
    if emotion == "frustrated":
        return "That sounds frustrating. Feel free to vent — I'm listening."
    if emotion == "positive":
        return "That's great to hear! 😊 What's making you feel good?"

    # === Stronger Fallback ===
    return ("Thanks for your question! I want to give you the best answer possible. "
            "Could you rephrase it or add a bit more detail? For example, try starting with 'What is', 'Who is', or 'Tell me about'.")

# ====================== UI (Sidebar, Header, Voice, Chat) ======================
with st.sidebar:
    st.header("MayBot Controls")
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hey again! How can I help you today?"}]
        st.session_state.last_topics = []
        st.rerun()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hey! How can I help you today?"}]
        st.session_state.last_topics = []
        st.rerun()
    st.divider()
    st.caption("Created by Mayon Oberoi • Nagpur, India")

if logo_img:
    st.image(logo_img, width=150)
st.markdown('<h1 class="main-title">MayBot</h1>', unsafe_allow_html=True)
st.caption("Your helpful AI companion")

# Quick Actions
cols = st.columns(4)
with cols[0]:
    if st.button("😂 Joke", use_container_width=True):
        st.session_state.messages.append({"role": "assistant", "content": random.choice(jokes)})
        st.rerun()
with cols[1]:
    if st.button("🌟 Fact", use_container_width=True):
        st.session_state.messages.append({"role": "assistant", "content": "🌟 " + random.choice(fun_facts)})
        st.rerun()

# Voice Input
if st.button("🎤 Speak Now", type="primary", use_container_width=True):
    voice_html = """
    <script>
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            window.location.search = "?voice=" + encodeURIComponent(transcript);
        };
        recognition.start();
    </script>
    """
    st.components.v1.html(voice_html, height=0)

if "voice" in st.query_params:
    transcript = st.query_params["voice"]
    if transcript:
        st.session_state.messages.append({"role": "user", "content": transcript})
        st.rerun()

# Chat Display
for idx, msg in enumerate(st.session_state.messages):
    avatar = logo_img if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            if st.button("🔊 Read Aloud", key=f"read_{idx}"):
                tts_html = f"""
                <script>
                    const utterance = new SpeechSynthesisUtterance(`{msg['content'].replace('`', '\\`')}`);
                    utterance.rate = 1.05; utterance.pitch = 1.1;
                    speechSynthesis.speak(utterance);
                </script>
                """
                st.components.v1.html(tts_html, height=0)

# Chat Input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=logo_img):
        with st.spinner("Thinking..."):
            time.sleep(0.6)
            response = get_best_response(prompt)
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
    
