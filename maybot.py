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
    [data-testid="stAppViewContainer"] {background: #020617;
        background-image: radial-gradient(circle at 25% 25%, rgba(16, 185, 129, 0.18) 0%, transparent 50%),
                          radial-gradient(circle at 75% 75%, rgba(59, 130, 246, 0.18) 0%, transparent 50%);}
    .stChatMessage {border-radius: 22px; box-shadow: 0 12px 45px rgba(0,0,0,0.7); padding: 18px 24px; border: 1px solid rgba(255,255,255,0.1);}
    .main-title {font-size: 4.2rem; font-weight: 900; background: linear-gradient(90deg, #10b981, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center;}
</style>
""", unsafe_allow_html=True)

def load_logo():
    return Image.open(logo_path) if os.path.exists(logo_path) else None

logo_img = load_logo()

# ====================== CONTENT ======================
jokes = ["Why don't skeletons fight? They don't have the guts! 😂", "Why did the scarecrow win? He was outstanding in his field! 🌾"]
fun_facts = ["Octopuses have three hearts!", "Honey never spoils!", "A group of flamingos is called a flamboyance."]
quotes = ["The only way to do great work is to love what you do. – Steve Jobs", "Be the change you wish to see in the world. – Mahatma Gandhi"]

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Arre waah! Hey yaar 😊 I'm MayBot, made with love by Mayon from Nagpur. Kaise ho aaj? How are you feeling?"}]

if "last_topics" not in st.session_state:
    st.session_state.last_topics = []
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "neutral"
if "chat_summary" not in st.session_state:
    st.session_state.chat_summary = ""

# ====================== ETHICAL + EMOTIONAL INTELLIGENCE ======================
def detect_emotion(text):
    t = text.lower()
    if any(w in t for w in ["frustrated", "angry", "annoyed", "irritated", "pissed"]): return "frustrated"
    if any(w in t for w in ["sad", "down", "depressed", "upset", "lonely", "bad day"]): return "sad"
    if any(w in t for w in ["anxious", "worried", "nervous", "overwhelmed"]): return "anxious"
    if any(w in t for w in ["happy", "great", "awesome", "excited", "amazing"]): return "positive"
    if any(w in t for w in ["confused", "lost", "don't understand"]): return "confused"
    return "neutral"

def get_best_response(user_query):
    q = user_query.strip()
    q_lower = q.lower()
    
    # Memory update
    st.session_state.last_topics.append(q_lower)
    if len(st.session_state.last_topics) > 10:
        st.session_state.last_topics.pop(0)
    
    emotion = detect_emotion(q)
    st.session_state.last_emotion = emotion

    # === 1. Greetings & Warm Connection ===
    if re.search(r'\b(hi|hello|hey|namaste|sup|kaise ho)\b', q_lower):
        if emotion == "positive": return "Heyy! Mast mood mein dikhte ho aaj 😄 Kya baat hai?"
        if emotion in ["sad", "frustrated", "anxious"]: return "Hey... lagta hai aaj thoda heavy feel ho raha hai. I'm here yaar. Batao kya hua?"
        return "Arre waah! Hello bhai! 😊 Aaj ka mood kaisa hai?"

    # === 2. Emotional Support (Ethical & Caring) ===
    ethical_note = "\n\n(Quick reminder: I'm an AI friend, not a therapist. If things feel heavy, please talk to a real person — family, friend, or call a helpline.)"

    if emotion == "sad":
        return f"That sounds really tough... It's okay to feel low sometimes. I'm here to listen if you want to share, but please also reach out to someone close to you.{ethical_note}"
    if emotion == "frustrated":
        return f"Ugh, frustration is the worst! Vent karo yaar — main sun raha hoon. But for real solutions, talking to someone in real life helps a lot.{ethical_note}"
    if emotion == "anxious":
        return f"Anxiety can feel overwhelming... Take a deep breath with me. I'm right here. If it's too much, please talk to someone who can truly support you.{ethical_note}"
    if emotion == "positive":
        return random.choice(["That's awesome yaar! 😄 Batao, kya mast cheez hui?", "Love this energy! Keep shining 🔥 What's making you smile?"])

    # === 3. Fun & Engagement ===
    if re.search(r'\b(joke|funny|hasi|mazak)\b', q_lower):
        return random.choice(jokes) + "\n\nHaha, lagi smile? Ek aur chahiye?"
    if re.search(r'\b(fact|interesting)\b', q_lower):
        return "🌟 Fun Fact: " + random.choice(fun_facts) + "\n\nMind blown? 😲"
    if re.search(r'\b(quote|motivation)\b', q_lower):
        return "💡 " + random.choice(quotes) + "\n\nFeels good, right?"

    # === 4. Math with Step-by-Step ===
    if any(c.isdigit() for c in q) or any(op in q_lower for op in ["+", "-", "*", "/", "^", "calculate", "solve"]):
        try:
            expr = q.replace('^', '**').replace('x', '*').replace('X', '*').replace(' ', '')
            if '=' in expr:
                left, right = expr.split('=', 1)
                result = sp.sympify(f"{left} - ({right})").evalf(12)
            else:
                result = sp.sympify(expr).evalf(12)
            clean = int(result) if result.is_integer else str(result).rstrip('0').rstrip('.')
            
            if "step" in q_lower or "explain" in q_lower or "how" in q_lower:
                return f"🔢 Answer: **{clean}**\n\nStep-by-step coming up if you want! Just say 'explain'."
            return f"🔢 The answer is **{clean}**. Mast solve hua na? Want me to explain the steps?"
        except:
            pass

    # === 5. Knowledge (Wikipedia) ===
    if any(word in q_lower for word in ["what is", "who is", "tell me about", "explain", "kya hai"]):
        try:
            term = re.sub(r'^(what is|who is|tell me about|explain|kya hai)\s+', '', q, flags=re.I).strip()
            titles = wikipedia.search(term, results=3)
            if titles:
                summary = wikipedia.summary(titles[0], sentences=7, auto_suggest=True)
                page = wikipedia.page(titles[0])
                return f"**{page.title}**\n\n{summary}\n\nSource: {page.url}\n\nAur kuch jaanna hai iske baare mein?"
        except:
            pass

    # === 6. Smart, Natural Fallback with Memory ===
    if st.session_state.last_topics:
        last = st.session_state.last_topics[-1]
        if "math" in last or "calculate" in last:
            return "Pehle math pe baat kar rahe the... ab kya soch rahe ho yaar?"
    
    return random.choice([
        "Hmm, interesting baat hai... Aur batao na, main sun raha hoon 😊",
        "Samajh gaya. Thoda aur detail doge to better help kar sakta hoon.",
        "Achha lag raha hai baat karna tere saath. Kya aur hai dil mein?"
    ])

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("MayBot Controls")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🆕 New Chat", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": "Fresh start! Hey yaar 😊 Kya scene hai aaj?"}]
            st.session_state.last_topics = []
            st.rerun()
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": "Clean slate! Hello again 😊 How are you feeling?"}]
            st.session_state.last_topics = []
            st.rerun()

    if st.button("📥 Export Chat", use_container_width=True):
        if len(st.session_state.messages) > 1:
            chat_text = "\n\n".join([f"{m['role'].upper()} ({datetime.now().strftime('%H:%M')}): {m['content']}" for m in st.session_state.messages])
            st.download_button("⬇️ Download", chat_text, f"MayBot_Chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", "text/plain", use_container_width=True)

    st.divider()
    st.caption("Made with ❤️ by Mayon Oberoi • Nagpur, India")

# ====================== HEADER ======================
if logo_img:
    st.image(logo_img, width=150)
st.markdown('<h1 class="main-title">MayBot</h1>', unsafe_allow_html=True)
st.caption("Your warm Nagpur buddy who actually listens 💙")

# ====================== QUICK ACTIONS ======================
st.markdown("### Quick Vibes")
cols = st.columns(4)
with cols[0]:
    if st.button("😂 Joke", use_container_width=True):
        st.session_state.messages.append({"role": "assistant", "content": random.choice(jokes) + "\n\nHaha, lagi?"})
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
    if st.button("🎤 Speak", type="primary", use_container_width=True):
        voice_html = """
        <script>
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-US';
            recognition.onresult = function(event) { window.location.search = "?voice=" + encodeURIComponent(event.results[0][0].transcript); };
            recognition.start();
        </script>
        """
        st.components.v1.html(voice_html, height=0)

# ====================== VOICE HANDLER ======================
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
                    utterance.rate = 1.05; utterance.pitch = 1.1; speechSynthesis.speak(utterance);
                </script>
                """
                st.components.v1.html(tts_html, height=0)

# ====================== CHAT INPUT ======================
if prompt := st.chat_input("Bolo yaar... what's on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=logo_img):
        with st.spinner("Thinking..."):
            time.sleep(0.6)  # natural pause
            response = get_best_response(prompt)
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
