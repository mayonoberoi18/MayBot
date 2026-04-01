import streamlit as st
from PIL import Image
import os
import wikipedia
import sympy as sp
import random

wikipedia.set_lang("en")

# ====================== PAGE CONFIG ======================
logo_path = "illuminati.png"

try:
    favicon = Image.open(logo_path)
except:
    favicon = "🤖"

st.set_page_config(page_title="MayBot", page_icon=favicon, layout="wide")

# Beautiful Dark Theme
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: #020617;
        background-image: radial-gradient(circle at 20% 30%, rgba(16, 185, 129, 0.15) 0%, transparent 50%),
                          radial-gradient(circle at 80% 70%, rgba(59, 130, 246, 0.18) 0%, transparent 50%);
    }
    .stChatMessage {
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        padding: 16px 20px;
    }
    .main-title {
        font-size: 3.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #10b981, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Load Logo
def load_logo():
    if os.path.exists(logo_path):
        try:
            return Image.open(logo_path)
        except:
            return None
    return None

logo_img = load_logo()

# ====================== FUN CONTENT ======================
jokes = [
    "Why don't skeletons fight each other? They don't have the guts! 😂",
    "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
    "I'm reading a book about anti-gravity. It's impossible to put down! 📖",
    "Why do programmers prefer dark mode? Because light attracts bugs! 💻",
    "Why did the math book look sad? Because it had too many problems! 📚",
    "Parallel lines have so much in common... It's a shame they'll never meet. 😌"
]

fun_facts = [
    "Octopuses have three hearts and blue blood!",
    "A flock of flamingos is called a flamboyance.",
    "Honey never spoils. Archaeologists found 3000-year-old honey that was still edible!",
    "Bananas are technically berries, but strawberries aren't.",
    "A single bolt of lightning contains enough energy to toast 100,000 slices of bread!"
]

quotes = [
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Be the change that you wish to see in the world. – Mahatma Gandhi",
    "In the middle of difficulty lies opportunity. – Albert Einstein",
    "Believe you can and you're halfway there. – Theodore Roosevelt"
]

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello there! I'm MayBot 😊 How are you doing today?"}]

# ====================== MAIN RESPONSE FUNCTION ======================
def get_vast_answer(user_query):
    q = user_query.strip().lower()
    
    if any(word in q for word in ["who made you", "creator", "founder", "mayon", "mayon oberoi"]):
        return "I'm MayBot, lovingly created by Mayon Oberoi from Nagpur, India. Thank you for asking! 🇮🇳 How can I make your day better?"

    # Math
    if any(c.isdigit() for c in user_query) and any(op in user_query for op in '+-*/^()=xX'):
        try:
            expr = user_query.replace('^', '**').replace('x', '*').replace('X', '*').replace(' ', '')
            if '=' in expr:
                left, right = expr.split('=', 1)
                result = sp.sympify(f"{left} - ({right})").evalf(10)
            else:
                result = sp.sympify(expr).evalf(10)
            clean = int(result) if result.is_integer else str(result).rstrip('0').rstrip('.')
            return f"🔢 The answer is **{clean}**.\n\nWould you like me to explain the steps?"
        except:
            pass

    # Wikipedia
    try:
        titles = wikipedia.search(user_query, results=3)
        if titles:
            summary = wikipedia.summary(titles[0], sentences=5, auto_suggest=False)
            return f"{summary.strip()}\n\nDid that help? Let me know if you want more details! 😊"
    except:
        pass

    return "Thank you for your message! I don't have all the answers, but I'm here with you. Could you tell me more about what you're thinking? 💙"

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("MayBot Controls")
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hello again! It's great to see you 😊 What’s on your mind?"}]
        st.rerun()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hello there! How can I help you today? 😊"}]
        st.rerun()
    
    st.divider()
    st.caption("Powered by Mayon Oberoi • Nagpur, India")

# ====================== HEADER ======================
if logo_img:
    st.image(logo_img, width=130)
st.markdown('<h1 class="main-title">MayBot</h1>', unsafe_allow_html=True)
st.caption("Powered by Mayon Oberoi")

# ====================== FUN BUTTONS ======================
st.markdown("**Have some fun with me!**")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🎭 Tell me a Joke", use_container_width=True):
        joke = random.choice(jokes)
        st.session_state.messages.append({"role": "assistant", "content": f"{joke}\n\nHaha! Want another one? 😄"})
        st.rerun()

with col2:
    if st.button("🌟 Fun Fact", use_container_width=True):
        fact = random.choice(fun_facts)
        st.session_state.messages.append({"role": "assistant", "content": f"Did you know? {fact}\n\nIsn't that cool? ✨"})
        st.rerun()

with col3:
    if st.button("💡 Motivational Quote", use_container_width=True):
        quote = random.choice(quotes)
        st.session_state.messages.append({"role": "assistant", "content": f"Here's a little inspiration:\n\n*{quote}*\n\nHope that brightens your day! 🌟"})
        st.rerun()

# ====================== VOICE INPUT ======================
st.markdown("### 🎤 Voice Input")
if st.button("🎤 Click & Speak", use_container_width=True):
    st.session_state.voice_mode = True

if st.session_state.get("voice_mode", False):
    voice_html = """
    <script>
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.start();
        recognition.onresult = function(event) {
            const text = event.results[0][0].transcript;
            window.parent.postMessage({type: "streamlit:setComponentValue", value: text}, "*");
        };
    </script>
    """
    st.components.v1.html(voice_html, height=0)
    st.session_state.voice_mode = False

# ====================== CHAT INTERFACE ======================
for msg in st.session_state.messages:
    avatar = logo_img if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=logo_img):
        with st.spinner("Thinking..."):
            response = get_vast_answer(prompt)
            st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
