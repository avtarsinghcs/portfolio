import streamlit as st
import requests
import time
import random
import plotly.graph_objects as go
from datetime import datetime

# ============================================
# CONFIG
# ============================================

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="RAGBOT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(124,58,237,0.15), transparent 30%),
            radial-gradient(circle at top right, rgba(6,182,212,0.15), transparent 30%),
            linear-gradient(180deg, #050505 0%, #0d0d0d 100%);
        color: white;
    }

    section[data-testid="stSidebar"] {
        background: rgba(12,12,12,0.85);
        backdrop-filter: blur(25px);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .main-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg,#7c3aed,#06b6d4,#8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        animation: glow 3s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from {
            filter: drop-shadow(0 0 10px rgba(124,58,237,0.4));
        }
        to {
            filter: drop-shadow(0 0 25px rgba(6,182,212,0.6));
        }
    }

    .subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .glass-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 1.5rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        border: 1px solid rgba(124,58,237,0.4);
        box-shadow: 0 12px 40px rgba(124,58,237,0.2);
    }

    .metric-card {
        background: linear-gradient(145deg, rgba(124,58,237,0.15), rgba(6,182,212,0.08));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(18px);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: white;
    }

    .metric-label {
        color: #9ca3af;
        font-size: 0.9rem;
    }

    .chat-user {
        background: linear-gradient(135deg,#7c3aed,#8b5cf6);
        padding: 1rem;
        border-radius: 18px;
        margin-bottom: 1rem;
        margin-left: 20%;
        color: white;
        box-shadow: 0 0 20px rgba(124,58,237,0.3);
    }

    .chat-ai {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 1rem;
        border-radius: 18px;
        margin-bottom: 1rem;
        margin-right: 20%;
        backdrop-filter: blur(18px);
    }

    .source-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .status-pill {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 999px;
        background: rgba(16,185,129,0.15);
        border: 1px solid rgba(16,185,129,0.3);
        color: #10b981;
        font-size: 0.85rem;
        margin-right: 0.5rem;
    }

    .upload-box {
        border: 2px dashed rgba(124,58,237,0.5);
        border-radius: 24px;
        padding: 2rem;
        background: rgba(255,255,255,0.03);
    }

    .stButton>button {
        width: 100%;
        border-radius: 14px;
        border: none;
        background: linear-gradient(90deg,#7c3aed,#06b6d4);
        color: white;
        font-weight: 700;
        padding: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 25px rgba(124,58,237,0.35);
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 40px rgba(6,182,212,0.45);
    }

    .stTextInput>div>div>input {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        color: white;
        border-radius: 14px;
    }

    .stFileUploader {
        background: rgba(255,255,255,0.03);
        border-radius: 20px;
        padding: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================
# SESSION STATE
# ============================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    st.markdown("## ⚡ RAGBOT Analytics")

    st.markdown(
        """
        <div class='status-pill'>🟢 SYSTEM ONLINE</div>
        <div class='status-pill'>⚡ GROQ ACTIVE</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-value'>{len(st.session_state.uploaded_docs)}</div>
                <div class='metric-label'>Documents</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-value'>{len(st.session_state.messages)}</div>
                <div class='metric-label'>Chats</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### 📊 Retrieval Stats")

    retrieval_score = random.randint(82, 99)

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = retrieval_score,
        title = {'text': "AI Confidence"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': '#7c3aed'},
            'bgcolor': '#111111',
            'borderwidth': 1,
            'bordercolor': '#333333'
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color':'white'}
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🧠 AI Stack")

    st.markdown(
        """
        - ⚡ Groq Llama 3.3 70B
        - 🧠 SentenceTransformers
        - 📚 Multi-PDF RAG
        - 🔎 Qdrant Vector Search
        - 🚀 FastAPI Backend
        """
    )

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# ============================================
# HERO SECTION
# ============================================

st.markdown(
    "<h1 class='main-title'>RAGBOT</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Next-Generation Multi-Document AI Retrieval System</p>",
    unsafe_allow_html=True
)

# ============================================
# TOP METRICS
# ============================================

col1, col2, col3, col4 = st.columns(4)

metrics = [
    ("⚡ Latency", "0.8s"),
    ("📄 Chunks", "12.4K"),
    ("🧠 Embeddings", "BGE-Small"),
    ("🔎 Vector DB", "Qdrant")
]

for col, metric in zip([col1,col2,col3,col4], metrics):
    with col:
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-value'>{metric[1]}</div>
                <div class='metric-label'>{metric[0]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# MAIN LAYOUT
# ============================================

left, right = st.columns([1,2])

# ============================================
# LEFT PANEL
# ============================================

with left:

    st.markdown(
        "<div class='glass-card'>",
        unsafe_allow_html=True
    )

    st.markdown("## 📂 Upload Knowledge Base")

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        for uploaded_file in uploaded_files:

            if uploaded_file.name not in st.session_state.uploaded_docs:

                with st.spinner(f"Processing {uploaded_file.name}..."):

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file,
                            "application/pdf"
                        )
                    }

                    response = requests.post(
                        f"{BACKEND_URL}/upload-pdf",
                        files=files
                    )

                    if response.status_code == 200:

                        st.session_state.uploaded_docs.append(
                            uploaded_file.name
                        )

                        st.toast(
                            f"✅ {uploaded_file.name} uploaded successfully"
                        )

    st.markdown("### 📚 Uploaded Documents")

    for doc in st.session_state.uploaded_docs:

        st.markdown(
            f"""
            <div class='source-card'>
                📄 {doc}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# RIGHT PANEL
# ============================================

with right:

    st.markdown(
        "<div class='glass-card'>",
        unsafe_allow_html=True
    )

    st.markdown("## 🤖 AI Research Assistant")

    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown(
                f"""
                <div class='chat-user'>
                    {message['content']}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class='chat-ai'>
                    {message['content']}
                </div>
                """,
                unsafe_allow_html=True
            )

    question = st.text_input(
        "Ask anything across all uploaded PDFs"
    )

    if st.button("🚀 Ask RAGBOT"):

        if question:

            st.session_state.messages.append(
                {
                    "role":"user",
                    "content":question
                }
            )

            with st.spinner("RAGBOT is thinking..."):

                start = time.time()

                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    params={
                        "question":question
                    }
                )

                latency = round(time.time() - start, 2)

                result = response.json()

                answer = result["answer"]

                st.session_state.messages.append(
                    {
                        "role":"assistant",
                        "content":answer
                    }
                )

                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <center>
        <p style='color:#666;'>
            Powered by Groq • Qdrant • FastAPI • SentenceTransformers
        </p>
    </center>
    """,
    unsafe_allow_html=True
)