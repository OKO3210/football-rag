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

    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0a2e 50%, #0d1b2a 100%);
        min-height: 100vh;
    }

    .main-title {
        font-family: 'Bebas Neue', cursive;
        font-size: 4rem;
        background: linear-gradient(90deg, #e4002b, #ffffff, #004c8c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: 4px;
        margin-bottom: 0;
        text-shadow: none;
    }

    .subtitle {
        text-align: center;
        color: #888;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        margin-bottom: 2rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .chat-message-user {
        background: linear-gradient(135deg, #004c8c, #0066cc);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px;
        margin: 8px 0;
        color: white;
        font-family: 'Inter', sans-serif;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(0, 76, 140, 0.3);
    }

    .chat-message-bot {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #e4002b33;
        border-radius: 18px 18px 18px 4px;
        padding: 12px 18px;
        margin: 8px 0;
        color: #e8e8e8;
        font-family: 'Inter', sans-serif;
        max-width: 85%;
        box-shadow: 0 4px 15px rgba(228, 0, 43, 0.1);
    }

    .bot-name {
        color: #e4002b;
        font-weight: 600;
        font-size: 0.8rem;
        margin-bottom: 4px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .psg-badge {
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .hint-box {
        background: rgba(228, 0, 43, 0.08);
        border-left: 3px solid #e4002b;
        border-radius: 4px;
        padding: 10px 15px;
        margin-bottom: 1.5rem;
        color: #aaa;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        font-style: italic;
    }

    div[data-testid="stChatInput"] {
        background: #1a1a2e;
        border: 1px solid #e4002b44;
        border-radius: 12px;
    }

    div[data-testid="stChatInput"] textarea {
        color: white !important;
        font-family: 'Inter', sans-serif;
    }

    .stButton button {
        background: linear-gradient(135deg, #e4002b, #cc0025);
        color: white;
        border: none;
        border-radius: 8px;
        font-family: 'Bebas Neue', cursive;
        letter-spacing: 2px;
        font-size: 1rem;
        padding: 8px 20px;
        transition: all 0.2s;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(228, 0, 43, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="psg-badge">⚽</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">PARISBOT</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Expert Football · Ultra PSG · Basé sur Wikipedia</p>', unsafe_allow_html=True)

st.markdown("""
<div class="hint-box">
    Donne-moi des indices sur un joueur, un club, une finale ou un événement football... et je devine !
    Exemple : "Une équipe a perdu 5-0 en finale de Ligue des Champions, tu sais de quelle finale je parle ?"
</div>
""", unsafe_allow_html=True)

if "rag" not in st.session_state:
    with st.spinner("Chargement de la base de connaissances..."):
        st.session_state.rag = RAG()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message-user">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div class="chat-message-bot">
                <div class="bot-name">⚽ ParisBot</div>
                {message["content"]}
            </div>
        ''', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col2:
    if st.button("Effacer"):
        st.session_state.messages = []
        st.rerun()

if user_input := st.chat_input("Donne-moi un indice..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-message-user">{user_input}</div>', unsafe_allow_html=True)

    with st.spinner("ParisBot réfléchit..."):
        response = st.session_state.rag.answer_question(user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown(f'''
        <div class="chat-message-bot">
            <div class="bot-name">⚽ ParisBot</div>
            {response}
        </div>
    ''', unsafe_allow_html=True)
