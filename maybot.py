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
    .stChatMessage {
        border-radius: 22px;
        box-shadow: 0 12px 45px rgba(0,0,0,0.7);
        padding: 18px 24px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .main-title {
        font-size: 4.2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #10b981, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def load_logo():
    return Image.open(logo_path) if os.path.exists(logo_path) else None

logo_img = load_logo()

# ====================== CONTENT ======================
jokes = [
    "Why don't skeletons fight each other? They don't have the guts! 😂",
    "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
    "Why do programmers prefer dark mode? Light attracts bugs! 💻"
]

fun_facts = [
    "Octopuses have three hearts!",
    "Honey never spoils!",
    "A group of flamingos is called a flamboyance."
]

quotes = [
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Be the change you wish to see in the world. – Mahatma Gandhi"
]

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hey! I'm MayBot 😊 Created by Mayon from Nagpur. Nice to meet you. How are you feeling today?"
    }]

if "last_topics" not in st.session_state:
    st.session_state.last_topics = []
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "neutral"

# ====================== REFINED EMOTION DETECTION ======================
def detect_emotion(text):
    t = text.lower()
    if any(w in t for w in ["frustrated", "angry", "annoyed", "irritated", "pissed"]):
        return "frustrated"
    if any(w in t for w in ["sad", "down", "depressed", "upset", "lonely", "bad day"]):
        return "sad"
    if any(w in t for w in ["anxious", "worried", "nervous", "overwhelmed"]):
        return "anxious"
    if any(w in t for w in ["happy", "great", "awesome", "excited", "amazing", "proud"]):
        return "positive"
    if any(w in t for w in ["confused", "lost", "don't understand"]):
        return "confused"
    return "neutral"

# ====================== BEST RESPONSE LOGIC ======================
def get_best_response(user_query):
    q = user_query.strip()
    q_lower = q.lower()

    # Update memory
    st.session_state.last_topics.append(q_lower)
    if len(st.session_state.last_topics) > 10:
        st.session_state.last_topics.pop(0)

    emotion = detect_emotion(q)
    st.session_state.last_emotion = emotion

    # Ethical note for sensitive topics
    ethical_note = "\n\nJust a reminder: I'm an AI companion, not a licensed therapist. If you're feeling overwhelmed, please talk to a friend, family member, or a mental health professional."

    # 1. Greetings
    if re.search(r'\b(hi|hello|hey|sup|good morning|good afternoon|good evening)\b', q_lower):
        if emotion == "positive":
            return "Hey! You sound in a great mood today 😊 What's making you happy?"
        elif emotion in ["sad", "frustrated", "anxious"]:
            return "Hey... You sound like you're having a tough day. How are you really doing?"
        return "Hey! Great to see you 😊 How are you feeling today?"

    if "how are you" in q_lower:
        return "I'm doing well, thank you for asking! How about you — how's your day going?"

    # 2. Thanks
    if any(word in q_lower for word in ["thank", "thanks", "thank you"]):
        return "You're very welcome! I'm happy I could help 😊"

    # 3. About Me
    if any(word in q_lower for word in ["who made you", "creator", "mayon", "your developer"]):
        return "I'm MayBot, created by Mayon Oberoi from Nagpur, India. He's a passionate developer who built me to be helpful and friendly. What made you curious?"

    # 4. Emotional Support (Ethical & Balanced)
    if emotion == "positive":
        return random.choice([
            "That's wonderful to hear! I'm really glad you're feeling good 😊 Tell me more about it!",
            "Love this positive energy! What's the best part of your day so far?"
        ])

    if emotion == "sad":
        return ("I'm really sorry you're feeling this way. It's completely okay to feel down sometimes. "
                "I'm here to listen if you'd like to share, but please also consider talking to someone close to you." + ethical_note)

    if emotion == "frustrated":
        return ("That sounds really frustrating... I can understand why you'd feel that way. "
                "Feel free to vent if it helps, but for deeper support, talking to a real person can make a big difference." + ethical_note)

    if emotion == "anxious":
        return ("Anxiety can feel heavy... You're not alone in feeling this. "
                "I'm here if you want to talk about it, but reaching out to someone in your life or a professional is often the most helpful step." + ethical_note)

    if emotion == "confused":
        return "I sense some confusion there. No worries — let's take it slow. What part feels unclear to you?"

    # 5. Fun Content
    if re.search(r'\b(joke|funny|make me laugh)\b', q_lower):
        if emotion in ["sad", "frustrated", "anxious"]:
            return "I know things might be tough right now, so here's a light joke to brighten the mood:\n\n" + random.choice(jokes) + "\n\nDid that help even a little?"
        return random.choice(jokes) + "\n\nHope that brought a smile! Want another one?"

    if re.search(r'\b(fun fact|interesting fact)\b', q_lower):
        return "🌟 Fun Fact: " + random.choice(fun_facts) + "\n\nPretty cool, right?"

    if re.search(r'\b(quote|motivation|inspire)\b', q_lower):
        return "💡 " + random.choice(quotes) + "\n\nHope this lifts your spirits a bit!"

    # 6. Math with Step-by-Step
    if any(c.isdigit() for c in q) or any(op in q_lower for op in ["+", "-", "*", "/", "^", "calculate", "solve"]):
        try:
            expr = q.replace('^', '**').replace('x', '*').replace('X', '*').replace(' ', '')
            if '=' in expr:
                left, right = expr.split('=', 1)
                result = sp.sympify(f"{left} - ({right})").evalf(12)
            else:
                result = sp.sympify(expr).evalf(12)
            clean = int(result) if result.is_integer else str(result).rstrip('0').rstrip('.')

            if any(word in q_lower for word in ["explain", "step", "how"]):
                return f"The answer is **{clean}**.\n\nWould you like me to show the step-by-step solution?"
            return f"The answer is **{clean}**. Nice question! Want me to explain how we got there?"
        except:
            pass

    # 7. Knowledge (Wikipedia)
    if any(word in q_lower for word in ["what is", "who is", "who was", "tell me about", "explain", "define"]):
        try:
            term = re.sub(r'^(what is|who is|tell me about|explain|define)\s+', '', q, flags=re.I).strip()
            titles = wikipedia.search(term, results=3)
            if titles:
                summary = wikipedia.summary(titles[0], sentences=7, auto_suggest=True)
                page = wikipedia.page(titles[0])
                return f"**{page.title}**\n\n{summary.strip()}\n\nSource: {page.url}\n\nIs there anything specific you'd like to know more about?"
        except:
            pass

    # 8. Natural & Warm Fallback
    return random.choice([
        "Hmm, interesting... Could you tell me a bit more? I'd love to understand better.",
        "Got it. Take your time — I'm here and listening 😊",
        "That's a good point. What made you think about this today?"
    ])

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("MayBot Controls")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🆕 New Chat", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": "Hey again! 😊 Fresh start — how are you feeling today?"}]
            st.session_state.last_topics = []
            st.rerun()
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": "Clean slate! Hello again 😊 How are you today?"}]
            st.session_state.last_topics = []
            st.rerun()

    if st.button("📥 Export Chat", use_container_width=True):
        if len(st.session_state.messages) > 1:
            chat_text = "\n\n".join([f"{m['role'].upper()} ({datetime.now().strftime('%H:%M')}): {m['content']}" for m in st.session_state.messages])
            st.download_button("⬇️ Download Conversation", chat_text,
                               f"MayBot_Chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", "text/plain", use_container_width=True)

    st.divider()
    st.caption("Created by Mayon Oberoi • Nagpur, India")

# ====================== HEADER ======================
if logo_img:
    st.image(logo_img, width=150)
st.markdown('<h1 class="main-title">MayBot</h1>', unsafe_allow_html=True)
st.caption("Your friendly, emotionally aware AI companion")

# ====================== QUICK ACTIONS ======================
st.markdown("### Quick Actions")
cols = st.columns(4)
with cols[0]:
    if st.button("😂 Joke", use_container_width=True):
        st.session_state.messages.append({"role": "assistant", "content": random.choice(jokes)})
        st.rerun()
with cols[1]:
    if st.button("🌟 Fact", use_container_width=True):
        st.session_state.messages.append({"role": "assistant", "content": "🌟 " + random.choice(fun_facts)})
        st.rerun()
with cols[2]:
    if st.button("💡 Quote", use_container_width=True):
        st.session_state.messages.append({"role": "assistant", "content": "💡 " + random.choice(quotes)})
        st.rerun()
with cols[3]:
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

# ====================== VOICE INPUT HANDLER ======================
if "voice" in st.query_params:
    transcript = st.query_params["voice"]
    if transcript:
        st.session_state.messages.append({"role": "user", "content": transcript})
        st.rerun()

# ====================== CHAT DISPLAY ======================
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

# ====================== MAIN CHAT INPUT ======================
if prompt := st.chat_input("What’s on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=logo_img):
        with st.spinner("Thinking..."):
            time.sleep(0.65)   # Natural human-like pause
            response = get_best_response(prompt)
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
