import streamlit as st
from rag import RAG

st.set_page_config(
    page_title="ParisBot - Expert Football",
    page_icon="⚽",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        color: #f0f0f0;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0a2e 50%, #0d1b2a 100%);
    }

    .main-title {
        font-family: 'Bebas Neue', cursive;
        font-size: 3.5rem;
        background: linear-gradient(90deg, #e4002b, #ffffff, #004c8c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        letter-spacing: 4px;
        margin: 0;
    }

    .subtitle {
        text-align: center;
        color: #888888;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        margin-bottom: 1.5rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hint-box {
        background: rgba(228, 0, 43, 0.08);
        border-left: 3px solid #e4002b;
        border-radius: 4px;
        padding: 10px 15px;
        margin-bottom: 1.5rem;
        color: #aaaaaa;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        font-style: italic;
    }

    .msg-user {
        background: linear-gradient(135deg, #004c8c, #0066cc);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px;
        margin: 8px 0 8px auto;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        max-width: 80%;
        width: fit-content;
        box-shadow: 0 4px 15px rgba(0, 76, 140, 0.3);
        margin-left: auto;
    }

    .msg-bot {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid rgba(228, 0, 43, 0.2);
        border-radius: 18px 18px 18px 4px;
        padding: 12px 18px;
        margin: 8px auto 8px 0;
        color: #e8e8e8 !important;
        font-family: 'Inter', sans-serif;
        max-width: 85%;
        width: fit-content;
        box-shadow: 0 4px 15px rgba(228, 0, 43, 0.1);
    }

    .bot-label {
        color: #e4002b;
        font-weight: 600;
        font-size: 0.75rem;
        margin-bottom: 6px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .stChatInput textarea {
        background-color: #1a1a2e !important;
        color: #f0f0f0 !important;
        border: 1px solid rgba(228, 0, 43, 0.3) !important;
        border-radius: 12px !important;
    }

    .stChatInput textarea::placeholder {
        color: #666666 !important;
    }

    section[data-testid="stChatInput"] {
        background: #0d0d1a !important;
        border-top: 1px solid rgba(228, 0, 43, 0.2);
    }

    .stButton > button {
        background: linear-gradient(135deg, #e4002b, #cc0025) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Bebas Neue', cursive !important;
        letter-spacing: 2px !important;
        font-size: 0.95rem !important;
        padding: 6px 16px !important;
    }

    .stSpinner > div {
        color: #e4002b !important;
    }

    p, div, span, label {
        color: #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center;font-size:3rem;margin-bottom:0">⚽</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">PARISBOT</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Expert Football · Ultra PSG · Basé sur Wikipedia</p>', unsafe_allow_html=True)

st.markdown("""
<div class="hint-box">
    💡 Donne-moi des indices sur un joueur, un club, une finale ou un événement football... et je devine !<br>
    <i>Exemple : "Une équipe a perdu 5-0 en finale de Ligue des Champions, tu sais de quelle finale je parle ?"</i>
</div>
""", unsafe_allow_html=True)

if "rag" not in st.session_state:
    with st.spinner("Chargement de la base de connaissances..."):
        st.session_state.rag = RAG()

if "messages" not in st.session_state:
    st.session_state.messages = []

_, col_btn = st.columns([6, 1])
with col_btn:
    if st.button("🗑 Reset"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="msg-user">{message["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="msg-bot"><div class="bot-label">⚽ ParisBot</div>{message["content"]}</div>',
            unsafe_allow_html=True
        )

if user_input := st.chat_input("Donne-moi un indice..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(
        f'<div class="msg-user">{user_input}</div>',
        unsafe_allow_html=True
    )

    with st.spinner("ParisBot réfléchit..."):
        response = st.session_state.rag.answer_question(user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown(
        f'<div class="msg-bot"><div class="bot-label">⚽ ParisBot</div>{response}</div>',
        unsafe_allow_html=True
    )
