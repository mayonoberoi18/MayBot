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

# Ultra Premium Dark UI
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: #020617;
        background-image: radial-gradient(circle at 25% 25%, rgba(16, 185, 129, 0.18) 0%, transparent 50%),
                          radial-gradient(circle at 75% 75%, rgba(59, 130, 246, 0.18) 0%, transparent 50%);
    }
    .stChatMessage {
        border-radius: 22px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.7);
        padding: 18px 22px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .main-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #10b981, #3b82f6, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -2px;
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

# Fun Content
jokes = ["Why don't skeletons fight each other? They don't have the guts! 😂", 
         "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
         "Why do programmers prefer dark mode? Because light attracts bugs! 💻"]

fun_facts = ["Octopuses have three hearts and blue blood!", 
             "Honey never spoils. 3000-year-old honey was found edible!",
             "A group of flamingos is called a flamboyance."]

quotes = ["The only way to do great work is to love what you do. – Steve Jobs",
          "Be the change you wish to see in the world. – Mahatma Gandhi",
          "In the middle of difficulty lies opportunity. – Albert Einstein"]

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm MayBot 😊 It's wonderful to meet you. How can I help you today?"}]

# ====================== ADVANCED INTELLIGENT RESPONSE ======================
def get_vast_answer(user_query):
    q = user_query.strip()
    q_lower = q.lower()

    # Identity
    if any(word in q_lower for word in ["who made you", "creator", "founder", "mayon", "mayon oberoi"]):
        return "I'm MayBot, proudly created by Mayon Oberoi from Nagpur, India. Thank you for asking! 🇮🇳 What can I do for you today?"

    # Jokes
    if any(word in q_lower for word in ["joke", "funny", "make me laugh"]):
        return random.choice(jokes) + "\n\nWould you like another one? 😄"

    # Fun Facts
    if any(word in q_lower for word in ["fun fact", "fact", "interesting"]):
        return "🌟 Fun Fact: " + random.choice(fun_facts) + "\n\nWant another one?"

    # Quotes
    if any(word in q_lower for word in ["quote", "motivation", "inspiration"]):
        return "💡 " + random.choice(quotes) + "\n\nHope this inspires you!"

    # Advanced Math
    if any(c.isdigit() for c in q) and any(op in q for op in '+-*/^()=xX'):
        try:
            expr = q.replace('^', '**').replace('x', '*').replace('X', '*').replace(' ', '')
            if '=' in expr:
                left, right = expr.split('=', 1)
                result = sp.sympify(f"{left} - ({right})").evalf(12)
            else:
                result = sp.sympify(expr).evalf(12)
            
            clean = int(result) if result.is_integer else str(result).rstrip('0').rstrip('.')
            return f"🔢 The answer is **{clean}**.\n\nWould you like me to explain the steps clearly?"
        except:
            pass

    # Links only when asked
    if any(word in q_lower for word in ["link", "source", "website", "url", "reference"]):
        try:
            titles = wikipedia.search(q, results=1)
            if titles:
                page = wikipedia.page(titles[0])
                return f"Here's a good source for you:\n\n**{page.title}**\n{page.url}"
        except:
            pass

    # Wikipedia Knowledge
    try:
        titles = wikipedia.search(q, results=3)
        if titles:
            summary = wikipedia.summary(titles[0], sentences=6, auto_suggest=False)
            return f"{summary.strip()}\n\nLet me know if you need more details or a link! 😊"
    except:
        pass

    # Smart & Gentle Fallback
    return "Thank you for your question! I'm thinking about it carefully. Could you please tell me a bit more so I can give you the best possible answer? I'm here to help 💙"

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("MayBot Controls")
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hello again! It's great to see you 😊 How can I help you today?"}]
        st.rerun()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm MayBot 😊 How can I help you today?"}]
        st.rerun()
    
    st.divider()
    st.caption("Powered by Mayon Oberoi • Nagpur, India")

# ====================== HEADER ======================
if logo_img:
    st.image(logo_img, width=140)
st.markdown('<h1 class="main-title">MayBot</h1>', unsafe_allow_html=True)
st.caption("Powered by Mayon Oberoi")

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
        recognition.onerror = function() {
            window.parent.postMessage({type: "streamlit:setComponentValue", value: "Sorry, I didn't catch that clearly. Please try again."}, "*");
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

# Main Chat Input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=logo_img):
        with st.spinner("Thinking..."):
            response = get_vast_answer(prompt)
            st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
