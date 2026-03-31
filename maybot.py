import streamlit as st
from PIL import Image
import os
from datetime import datetime
import wikipedia
from duckduckgo_search import DDGS
import sympy as sp

# Force English only
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

# ====================== PREMIUM CSS ======================
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: #020617;
        background-image:
            radial-gradient(circle at 20% 30%, rgba(16, 185, 129, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(59, 130, 246, 0.18) 0%, transparent 50%);
        background-attachment: fixed;
    }
    .stChatMessage {
        border-radius: 20px !important;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        border: 1px solid rgba(255,255,255,0.1);
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

# ====================== SAFE LOGO LOADING ======================
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
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# ====================== IMPROVED ANSWER FUNCTION ======================
def get_vast_answer(user_query):
    q = user_query.strip()
    
    if any(x in q.lower() for x in ["who made you", "creator", "founder", "mayon", "mayon oberoi"]):
        return "I am **MayBot**, an intelligent assistant created by **Mayon Oberoi** from Nagpur, India. 🇮🇳"

    # Math
    if any(c.isdigit() for c in q) and any(op in q for op in '+-*/^()=x'):
        try:
            expr = q.replace('^', '**').replace('x', '*').replace(' ', '')
            if '=' in expr:
                left, right = expr.split('=', 1)
                result = sp.sympify(f"{left}-({right})").evalf(10)
            else:
                result = sp.sympify(expr).evalf(10)
            return f"🔢 **Math Solution:**\n`{result}`"
        except:
            pass

    # Wikipedia (Priority)
    try:
        titles = wikipedia.search(q, results=3)
        if titles:
            summary = wikipedia.summary(titles[0], sentences=6, auto_suggest=False)
            return f"📖 **Wikipedia:**\n\n{summary.strip()}"
    except:
        pass

    # Web Search Fallback
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(q, max_results=5))
            if results:
                text = "\n\n".join([f"**{r.get('title','')}**\n{r.get('body','')}" for r in results if r.get('body')])
                return f"🌐 **Web Results:**\n\n{text[:1700]}..."
    except:
        pass

    return "I searched reliable sources but couldn't find a precise answer. Please rephrase your question in English."

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("🛠️ Controls")
    
    if st.button("🆕 New Chat", use_container_width=True):
        if st.session_state.messages:
            title = st.session_state.messages[0]["content"][:40] + "..." if len(st.session_state.messages[0]["content"]) > 40 else st.session_state.messages[0]["content"]
            st.session_state.chat_history.append({
                "id": st.session_state.current_chat_id,
                "title": title,
                "messages": st.session_state.messages.copy()
            })
        st.session_state.messages = []
        st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.rerun()

    if st.button("🗑️ Clear Current Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.subheader("📜 Recent Chats")
    for chat in reversed(st.session_state.chat_history[-8:]):
        if st.button(chat["title"], key=chat["id"], use_container_width=True):
            st.session_state.messages = chat["messages"].copy()
            st.rerun()

    st.divider()
    if st.button("📥 Export Chat", use_container_width=True) and st.session_state.messages:
        text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button("⬇️ Download TXT", text, f"MayBot_Chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", "text/plain")

    st.divider()
    st.caption("English Only • By Mayon Oberoi • Nagpur")

# ====================== MAIN UI ======================
if logo_img:
    st.image(logo_img, width=130)
else:
    st.markdown("<h1 style='text-align:center; font-size:4.5rem;'>🤖</h1>", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">MayBot</h1>', unsafe_allow_html=True)
st.caption("Accurate • Intelligent • English Only • Powered by Mayon Oberoi")

# Quick Prompts
st.markdown("**Quick Questions:**")
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("Solve 2x² + 5x - 3 = 0", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Solve 2x² + 5x - 3 = 0"})
        st.rerun()
with c2:
    if st.button("Latest AI news", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Latest AI news 2026"})
        st.rerun()
with c3:
    if st.button("About Nagpur", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Tell me about Nagpur India"})
        st.rerun()
with c4:
    if st.button("Who is Mayon?", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Who is Mayon Oberoi?"})
        st.rerun()

# Chat Display
for msg in st.session_state.messages:
    avatar = logo_img if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask me anything in English..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant", avatar=logo_img):
        with st.spinner("Searching accurate information..."):
            response = get_vast_answer(prompt)
            st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
