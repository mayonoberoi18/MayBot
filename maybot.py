import streamlit as st
from PIL import Image
import os
import wikipedia
import sympy as sp
from datetime import datetime

wikipedia.set_lang("en")

# ====================== PAGE CONFIG ======================
logo_path = "illuminati.png"

try:
    favicon = Image.open(logo_path)
except:
    favicon = "🤖"

st.set_page_config(
    page_title="MayBot",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Dark Theme
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: #020617 !important;
        background-image:
            radial-gradient(circle at 20% 30%, rgba(16, 185, 129, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(59, 130, 246, 0.18) 0%, transparent 50%);
    }
    .stChatMessage {
        border-radius: 20px !important;
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

# ====================== LOAD LOGO ======================
def load_logo():
    if os.path.exists(logo_path):
        try:
            return Image.open(logo_path)
        except:
            return None
    return None

logo_img = load_logo()

# ====================== SESSION STATE ======================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm MayBot. How can I help you today? 😊"}]

# ====================== SMART & POLITE RESPONSE FUNCTION ======================
def get_vast_answer(user_query):
    q = user_query.strip()
    
    if any(x in q.lower() for x in ["who made you", "creator", "founder", "mayon", "mayon oberoi"]):
        return "I'm MayBot, proudly created by Mayon Oberoi from Nagpur, India. It's a pleasure to chat with you! 🇮🇳 How may I help you today?"

    # Clean Math Solver
    if any(c.isdigit() for c in q) and any(op in q for op in '+-*/^()=xX'):
        try:
            expr = q.replace('^', '**').replace('x', '*').replace('X', '*').replace(' ', '')
            if '=' in expr:
                left, right = expr.split('=', 1)
                result = sp.sympify(f"{left} - ({right})").evalf(10)
            else:
                result = sp.sympify(expr).evalf(10)
            
            # Clean output
            if result.is_integer:
                clean_result = int(result)
            else:
                clean_result = str(result).rstrip('0').rstrip('.') if '.' in str(result) else str(result)
                
            return f"🔢 **Solution:** {clean_result}\n\nWould you like me to explain the steps?"
        except:
            pass

    # Wikipedia
    try:
        titles = wikipedia.search(q, results=3)
        if titles:
            summary = wikipedia.summary(titles[0], sentences=6, auto_suggest=False)
            return f"📖 Here's what I found:\n\n{summary.strip()}\n\nIs there anything else you'd like to know?"
    except:
        pass

    # Gentle Fallback
    return "Thank you for your question! I couldn't find a clear answer right now. Could you please rephrase it? I'm here and happy to help 😊"

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("🛠️ Controls")
    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today? 😊"}]
        st.rerun()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today? 😊"}]
        st.rerun()
    
    st.divider()
    st.caption("Powered by Mayon Oberoi • Nagpur, India")

# ====================== MAIN HEADER ======================
if logo_img:
    st.image(logo_img, width=130)
st.markdown('<h1 class="main-title">MayBot</h1>', unsafe_allow_html=True)
st.caption("Powered by Mayon Oberoi")

# ====================== VOICE INPUT ======================
st.markdown("**🎤 Voice Input**")
if st.button("🎤 Click to Speak", use_container_width=True):
    st.session_state.voice_mode = True

# JavaScript for Voice Recognition
if st.session_state.get("voice_mode", False):
    voice_html = """
    <script>
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            window.parent.postMessage({type: "streamlit:setComponentValue", value: transcript}, "*");
        };
        
        recognition.onerror = function() {
            window.parent.postMessage({type: "streamlit:setComponentValue", value: "Sorry, I couldn't hear you clearly."}, "*");
        };
        
        recognition.start();
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
