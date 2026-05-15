import streamlit as st
import time
from pipeline import run_research_pipeline
import base64
from datetime import datetime
import json

# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="Research AI | Premium Investigative Analysis",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# ULTRA PREMIUM CSS - AESTHETIC MASTERPIECE
# =========================================

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Cormorant+Garamond:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body {
        overflow-x: hidden;
    }
    
    /* ============================================
       PREMIUM COLOR PALETTE
       ============================================ */
    :root {
        --primary-gradient: linear-gradient(135deg, #00D9FF 0%, #0066FF 50%, #9D00FF 100%);
        --dark-gradient: linear-gradient(135deg, #0A0E27 0%, #0F1B2E 50%, #0D1624 100%);
        --glass-bg: rgba(10, 14, 39, 0.7);
        --glass-border: rgba(0, 217, 255, 0.15);
        
        --accent-1: #00D9FF;
        --accent-2: #0066FF;
        --accent-3: #9D00FF;
        --accent-4: #FF006E;
        
        --text-primary: #FFFFFF;
        --text-secondary: #E0E6F0;
        --text-tertiary: #A0A8B8;
    }
    
    /* ============================================
       HIDE STREAMLIT DEFAULT UI
       ============================================ */
    #MainMenu, footer, header {
        visibility: hidden;
        display: none;
    }
    
    /* ============================================
       BODY & MAIN BACKGROUND
       ============================================ */
    body, .main {
        background: var(--dark-gradient) !important;
        color: var(--text-primary);
        font-family: 'Syne', sans-serif;
    }
    
    .main {
        position: relative;
        overflow: hidden;
    }
    
    /* Animated background overlay */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(0, 217, 255, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(157, 0, 255, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(0, 102, 255, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* ============================================
       SIDEBAR STYLING
       ============================================ */
    .sidebar .sidebar-content {
        background: rgba(10, 14, 39, 0.5) !important;
        border-right: 1px solid var(--glass-border) !important;
        backdrop-filter: blur(20px) !important;
    }
    
    /* ============================================
       TYPOGRAPHY - PREMIUM
       ============================================ */
    h1 {
        font-family: 'Cormorant Garamond', serif;
        font-size: 4.5rem !important;
        font-weight: 700 !important;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.03em;
        margin-bottom: 0.3rem !important;
        text-shadow: 0 0 40px rgba(0, 217, 255, 0.2);
        animation: titleGlow 3s ease-in-out infinite;
    }
    
    @keyframes titleGlow {
        0%, 100% { text-shadow: 0 0 40px rgba(0, 217, 255, 0.2); }
        50% { text-shadow: 0 0 60px rgba(0, 217, 255, 0.4); }
    }
    
    h2 {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        color: var(--accent-1) !important;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #00D9FF, #0066FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h3 {
        font-family: 'Syne', sans-serif;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #00D9FF, #9D00FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    p {
        font-family: 'Syne', sans-serif;
        color: var(--text-secondary);
        line-height: 1.7;
        font-weight: 400;
    }
    
    /* ============================================
       INPUT STYLING - GLASSMORPHISM
       ============================================ */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid var(--glass-border) !important;
        border-radius: 20px !important;
        color: var(--text-primary) !important;
        font-size: 1.1rem !important;
        padding: 16px 24px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.3) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border: 2px solid var(--accent-1) !important;
        box-shadow: 
            0 0 0 4px rgba(0, 217, 255, 0.15),
            0 8px 32px rgba(0, 217, 255, 0.2) !important;
        background: rgba(0, 217, 255, 0.05) !important;
        transform: translateY(-2px);
    }
    
    /* ============================================
       BUTTON STYLING - PREMIUM
       ============================================ */
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: var(--text-primary) !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 16px 40px !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        font-family: 'Syne', sans-serif !important;
        letter-spacing: 0.5px;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 
            0 8px 32px rgba(0, 217, 255, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 
            0 16px 48px rgba(0, 217, 255, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(0.98);
    }
    
    /* ============================================
       PREMIUM CARD STYLING
       ============================================ */
    .card {
        background: linear-gradient(135deg, rgba(10, 14, 39, 0.6), rgba(15, 27, 46, 0.4)) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 24px !important;
        padding: 32px !important;
        margin: 20px 0 !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.2),
            0 0 1px rgba(0, 217, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.05) 0%, transparent 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
        pointer-events: none;
    }
    
    .card:hover {
        border-color: rgba(0, 217, 255, 0.4) !important;
        box-shadow: 
            0 16px 48px rgba(0, 217, 255, 0.2),
            0 0 1px rgba(0, 217, 255, 0.2) !important;
        transform: translateY(-8px);
    }
    
    .card:hover::before {
        opacity: 1;
    }
    
    /* ============================================
       METRIC CARDS - ULTRA PREMIUM
       ============================================ */
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.08), rgba(157, 0, 255, 0.06)) !important;
        border: 1.5px solid rgba(0, 217, 255, 0.25) !important;
        border-radius: 20px !important;
        padding: 28px 20px !important;
        text-align: center !important;
        transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        backdrop-filter: blur(15px) !important;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(0, 217, 255, 0.3) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .metric-card:hover {
        border-color: var(--accent-1) !important;
        box-shadow: 
            0 12px 40px rgba(0, 217, 255, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        transform: translateY(-8px) scale(1.05) !important;
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-card h3 {
        margin-top: 0 !important;
        font-size: 2.5rem !important;
        margin-bottom: 8px !important;
    }
    
    .metric-card p {
        color: var(--text-tertiary);
        margin: 0 0 12px 0 !important;
        font-size: 0.95rem !important;
    }
    
    .metric-card h2 {
        margin: 8px 0 0 0 !important;
        font-size: 1.8rem !important;
    }
    
    /* ============================================
       TAB STYLING - PREMIUM
       ============================================ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px !important;
        border-bottom: 2px solid rgba(0, 217, 255, 0.1) !important;
        background: linear-gradient(90deg, rgba(0, 217, 255, 0.02) 0%, transparent 100%);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 16px 28px !important;
        border-radius: 16px 16px 0 0 !important;
        background-color: transparent !important;
        border: none !important;
        color: var(--text-tertiary) !important;
        font-weight: 600 !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 1rem !important;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--primary-gradient);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--accent-1) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.15), rgba(0, 102, 255, 0.1)) !important;
        color: var(--accent-1) !important;
        border: 1px solid rgba(0, 217, 255, 0.2) !important;
        border-bottom: 3px solid var(--accent-1) !important;
        box-shadow: 0 8px 24px rgba(0, 217, 255, 0.15);
    }
    
    /* ============================================
       URL CARD STYLING
       ============================================ */
    .url-card {
        background: linear-gradient(135deg, rgba(0, 102, 255, 0.1), rgba(0, 217, 255, 0.05)) !important;
        border-left: 4px solid var(--accent-2) !important;
        border-radius: 16px !important;
        padding: 18px 20px !important;
        margin: 12px 0 !important;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(0, 217, 255, 0.1);
        border-right: 1px solid rgba(0, 217, 255, 0.1);
        border-bottom: 1px solid rgba(0, 217, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .url-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(180deg, var(--accent-2), var(--accent-1));
        transform: scaleY(0);
        transform-origin: top;
        transition: transform 0.4s ease;
    }
    
    .url-card:hover {
        background: linear-gradient(135deg, rgba(0, 102, 255, 0.2), rgba(0, 217, 255, 0.1)) !important;
        transform: translateX(8px);
        box-shadow: 0 8px 24px rgba(0, 217, 255, 0.2);
        border-left-color: var(--accent-1) !important;
    }
    
    .url-card:hover::before {
        transform: scaleY(1);
    }
    
    /* ============================================
       PROGRESS BAR - ANIMATED
       ============================================ */
    .stProgress > div > div > div > div {
        background: var(--primary-gradient) !important;
        border-radius: 20px !important;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.4);
        animation: progressPulse 2s ease-in-out infinite;
    }
    
    @keyframes progressPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 217, 255, 0.4); }
        50% { box-shadow: 0 0 40px rgba(0, 217, 255, 0.6); }
    }
    
    /* ============================================
       BADGE STYLING
       ============================================ */
    .badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        font-family: 'Syne', sans-serif;
        margin-right: 10px;
        margin-bottom: 10px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .badge-success {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.25), rgba(16, 185, 129, 0.1));
        color: #10B981;
        border: 1.5px solid #10B981;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.25), rgba(245, 158, 11, 0.1));
        color: #F59E0B;
        border: 1.5px solid #F59E0B;
    }
    
    .badge-info {
        background: linear-gradient(135deg, rgba(0, 102, 255, 0.25), rgba(0, 217, 255, 0.1));
        color: #0066FF;
        border: 1.5px solid #0066FF;
    }
    
    .badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 217, 255, 0.2);
    }
    
    /* ============================================
       DIVIDER - GRADIENT
       ============================================ */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(0, 217, 255, 0.3), 
            transparent);
        margin: 2.5rem 0;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.1);
    }
    
    /* ============================================
       SCROLLBAR - CUSTOM
       ============================================ */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 217, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--accent-1), var(--accent-2));
        border-radius: 10px;
        border: 3px solid transparent;
        background-clip: padding-box;
        box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--accent-2), var(--accent-3));
        background-clip: padding-box;
        box-shadow: 0 0 30px rgba(0, 217, 255, 0.5);
    }
    
    /* ============================================
       STATUS STYLING
       ============================================ */
    .stStatus {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05)) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-radius: 16px !important;
    }
    
    /* ============================================
       CODE BLOCK STYLING
       ============================================ */
    .stCodeBlock, .stMarkdown code {
        background: rgba(10, 14, 39, 0.8) !important;
        border: 1px solid rgba(0, 217, 255, 0.2) !important;
        border-radius: 16px !important;
        font-family: 'JetBrains Mono', monospace !important;
        padding: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* ============================================
       ANIMATIONS
       ============================================ */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes glowPulse {
        0%, 100% {
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
        }
        50% {
            box-shadow: 0 0 40px rgba(0, 217, 255, 0.6);
        }
    }
    
    /* Apply animations */
    .stColumn > * {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# =========================================
# SESSION STATE INITIALIZATION
# =========================================

if "research_results" not in st.session_state:
    st.session_state.research_results = None

if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

if "step_progress" not in st.session_state:
    st.session_state.step_progress = {
        "search": False,
        "scrape": False,
        "write": False,
        "critique": False
    }

# =========================================
# PREMIUM SIDEBAR
# =========================================

with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h3 style='margin: 0; font-size: 1.5rem;'>⚙️ Control Panel</h3>
        <p style='color: #A0A8B8; margin-top: 5px; font-size: 0.9rem;'>Fine-tune your research</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Status Card
    st.markdown("<h3 style='margin-bottom: 10px;'>📊 Research Status</h3>", unsafe_allow_html=True)
    
    if st.session_state.research_results:
        st.markdown("""
        <div class='metric-card' style='margin-bottom: 15px;'>
            <span style='color: #10B981; font-size: 1.5rem;'>✅</span><br>
            <p style='color: #10B981; font-weight: 700; margin: 8px 0;'>Analysis Complete</p>
            <p style='margin: 0; color: #A0A8B8; font-size: 0.85rem;'>Ready to explore</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sources Found", len(st.session_state.research_results.get("urls", [])))
        with col2:
            words = len(st.session_state.research_results.get("report", "").split())
            st.metric("Words Analyzed", f"{words:,}")
    else:
        st.markdown("""
        <div class='metric-card' style='margin-bottom: 15px;'>
            <span style='color: #F59E0B; font-size: 1.5rem;'>⏳</span><br>
            <p style='color: #F59E0B; font-weight: 700; margin: 8px 0;'>Awaiting Input</p>
            <p style='margin: 0; color: #A0A8B8; font-size: 0.85rem;'>Start a new research</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # How It Works
    st.markdown("<h3 style='margin-bottom: 15px;'>🚀 Research Pipeline</h3>", unsafe_allow_html=True)
    
    steps = [
        ("🔍", "Web Search", "Find relevant articles"),
        ("📰", "Extract Content", "Scrape & clean data"),
        ("✍️", "Generate Report", "Write analysis"),
        ("🎯", "Expert Critique", "Quality review")
    ]
    
    for emoji, title, desc in steps:
        st.markdown(f"""
        <div style='padding: 12px 0; border-bottom: 1px solid rgba(0, 217, 255, 0.1);'>
            <p style='margin: 0; font-weight: 700;'>{emoji} {title}</p>
            <p style='margin: 4px 0 0 0; font-size: 0.8rem; color: #A0A8B8;'>{desc}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Settings
    st.markdown("<h3 style='margin-bottom: 15px;'>⚡ Performance</h3>", unsafe_allow_html=True)
    
    quality = st.select_slider(
        "Analysis Depth",
        options=["🚀 Fast", "⚡ Balanced", "🔬 Deep"],
        value="⚡ Balanced"
    )
    
    st.divider()
    
    st.markdown("""
    <div style='padding: 15px; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1), rgba(157, 0, 255, 0.05)); border-radius: 16px; border: 1px solid rgba(0, 217, 255, 0.2);'>
        <h4 style='margin: 0 0 10px 0; font-size: 0.95rem;'>✨ Premium Features</h4>
        <ul style='margin: 0; padding-left: 20px; font-size: 0.85rem; color: #A0A8B8;'>
            <li>Multi-format export</li>
            <li>Real-time progress</li>
            <li>Advanced analytics</li>
            <li>Expert critique</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# MAIN CONTENT - ULTRA PREMIUM
# =========================================

# Animated Hero Section
st.markdown("""
<div style='text-align: center; padding: 60px 20px 40px 20px; position: relative; z-index: 1;'>
    <h1 style='animation: titleGlow 3s ease-in-out infinite;'>✨ Research AI</h1>
    <p style='font-size: 1.2rem; color: var(--text-secondary); margin-top: -15px; letter-spacing: 0.5px;'>
        Next-Generation Investigative Research Platform
    </p>
    <p style='color: var(--text-tertiary); margin-top: 12px; font-size: 1rem;'>
        🔍 Search • 📰 Analyze • ✍️ Report • 🎯 Critique
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Premium Input Section
st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>📝 Begin Your Research</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1], gap="large")

with col1:
    research_topic = st.text_input(
        "Enter your research topic:",
        placeholder="e.g., 'Quantum Computing Breakthroughs', 'AI Regulation Trends', 'Climate Tech Innovation'...",
        label_visibility="collapsed",
        key="topic_input"
    )

with col2:
    st.markdown("<div style='padding-top: 12px;'></div>", unsafe_allow_html=True)
    search_button = st.button("🚀 Launch", use_container_width=True, key="search_btn")

# =========================================
# RESEARCH EXECUTION - PREMIUM EXPERIENCE
# =========================================

if search_button and research_topic:
    st.session_state.is_loading = True
    
    # Premium progress section
    st.divider()
    
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='margin-bottom: 10px;'>🔄 Activating Research Pipeline</h2>
        <p style='color: var(--text-tertiary);'>Initiating 4-step analysis protocol...</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress tracking with premium design
    progress_col1, progress_col2, progress_col3, progress_col4 = st.columns(4, gap="small")
    
    steps_data = [
        (progress_col1, "🔍", "Search", "Discovering sources"),
        (progress_col2, "📰", "Extract", "Processing content"),
        (progress_col3, "✍️", "Analyze", "Generating report"),
        (progress_col4, "🎯", "Critique", "Quality review"),
    ]
    
    step_placeholders = []
    for col, emoji, title, desc in steps_data:
        with col:
            placeholder = st.empty()
            step_placeholders.append((placeholder, title))
            placeholder.markdown(f"""
            <div class='metric-card' style='background: linear-gradient(135deg, rgba(157, 0, 255, 0.15), rgba(0, 217, 255, 0.05));'>
                <p style='font-size: 2rem; margin: 0;'>{emoji}</p>
                <p style='margin: 8px 0 0 0; font-weight: 700; color: var(--accent-1);'>{title}</p>
                <p style='margin: 4px 0 0 0; font-size: 0.75rem; color: var(--text-tertiary);'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    try:
        # Overall progress bar
        overall_progress = st.progress(0)
        
        # Step 1: Search
        with st.spinner("🔍 Searching web for relevant articles..."):
            step_placeholders[0][0].markdown(f"""
            <div class='metric-card' style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.05)); animation: glowPulse 1.5s ease-in-out infinite;'>
                <p style='font-size: 2rem; margin: 0;'>🔍</p>
                <p style='margin: 8px 0 0 0; font-weight: 700; color: #10B981;'>Search</p>
                <p style='margin: 4px 0 0 0; font-size: 0.75rem; color: #10B981;'>In Progress...</p>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.3)
        
        overall_progress.progress(25)
        
        step_placeholders[0][0].markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));'>
            <p style='font-size: 2rem; margin: 0;'>✅</p>
            <p style='margin: 8px 0 0 0; font-weight: 700; color: #10B981;'>Search</p>
            <p style='margin: 4px 0 0 0; font-size: 0.75rem; color: #10B981;'>Complete</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 2: Scrape
        with st.spinner("📰 Extracting article content..."):
            step_placeholders[1][0].markdown(f"""
            <div class='metric-card' style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.05)); animation: glowPulse 1.5s ease-in-out infinite;'>
                <p style='font-size: 2rem; margin: 0;'>📰</p>
                <p style='margin: 8px 0 0 0; font-weight: 700; color: #10B981;'>Extract</p>
                <p style='margin: 4px 0 0 0; font-size: 0.75rem; color: #10B981;'>In Progress...</p>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.3)
        
        overall_progress.progress(50)
        
        step_placeholders[1][0].markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));'>
            <p style='font-size: 2rem; margin: 0;'>✅</p>
            <p style='margin: 8px 0 0 0; font-weight: 700; color: #10B981;'>Extract</p>
            <p style='margin: 4px 0 0 0; font-size: 0.75rem; color: #10B981;'>Complete</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 3: Write Report
        with st.spinner("✍️ Generating analytical report..."):
            step_placeholders[2][0].markdown(f"""
            <div class='metric-card' style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.05)); animation: glowPulse 1.5s ease-in-out infinite;'>
                <p style='font-size: 2rem; margin: 0;'>✍️</p>
                <p style='margin: 8px 0 0 0; font-weight: 700; color: #10B981;'>Analyze</p>
                <p style='margin: 4px 0 0 0; font-size: 0.75rem; color: #10B981;'>In Progress...</p>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.3)
        
        overall_progress.progress(75)
        
        # Execute the actual pipeline
        st.session_state.research_results = run_research_pipeline(research_topic)
        
        step_placeholders[2][0].markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));'>
            <p style='font-size: 2rem; margin: 0;'>✅</p>
            <p style='margin: 8px 0 0 0; font-weight: 700; color: #10B981;'>Analyze</p>
            <p style='margin: 4px 0 0 0; font-size: 0.75rem; color: #10B981;'>Complete</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 4: Critique
        with st.spinner("🎯 Conducting expert review..."):
            step_placeholders[3][0].markdown(f"""
            <div class='metric-card' style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.05)); animation: glowPulse 1.5s ease-in-out infinite;'>
                <p style='font-size: 2rem; margin: 0;'>🎯</p>
                <p style='margin: 8px 0 0 0; font-weight: 700; color: #10B981;'>Critique</p>
                <p style='margin: 4px 0 0 0; font-size: 0.75rem; color: #10B981;'>In Progress...</p>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.3)
        
        overall_progress.progress(100)
        
        step_placeholders[3][0].markdown(f"""
        <div class='metric-card' style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));'>
            <p style='font-size: 2rem; margin: 0;'>✅</p>
            <p style='margin: 8px 0 0 0; font-weight: 700; color: #10B981;'>Critique</p>
            <p style='margin: 4px 0 0 0; font-size: 0.75rem; color: #10B981;'>Complete</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.session_state.is_loading = False
        
        # Success message
        st.markdown("""
        <div style='text-align: center; padding: 20px; margin-top: 20px;'>
            <p style='font-size: 1.3rem; color: #10B981; font-weight: 700;'>✨ Research Complete!</p>
            <p style='color: var(--text-tertiary); margin-top: 8px;'>Your analysis is ready to explore below</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Error during research: {str(e)}")
        st.session_state.is_loading = False

# =========================================
# RESULTS DISPLAY - PREMIUM DASHBOARD
# =========================================

if st.session_state.research_results:
    st.divider()
    
    results = st.session_state.research_results
    
    # Stunning Metrics Dashboard
    st.markdown("""
    <div style='text-align: center; padding: 30px 0 20px 0;'>
        <h2 style='margin: 0;'>📊 Research Overview</h2>
        <p style='color: var(--text-tertiary); margin-top: 8px;'>Key statistics and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Metric Cards with Premium Styling
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4, gap="medium")
    
    with metric_col1:
        st.markdown(f"""
        <div class='metric-card'>
            <p style='font-size: 2.5rem; margin: 0;'>🔗</p>
            <p style='margin: 12px 0 6px 0; color: var(--text-tertiary); font-size: 0.9rem;'>Sources Found</p>
            <h2 style='margin: 0; font-size: 2rem; background: linear-gradient(135deg, #00D9FF, #0066FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{len(results["urls"])}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        words = len(results["report"].split())
        st.markdown(f"""
        <div class='metric-card'>
            <p style='font-size: 2.5rem; margin: 0;'>📄</p>
            <p style='margin: 12px 0 6px 0; color: var(--text-tertiary); font-size: 0.9rem;'>Report Length</p>
            <h2 style='margin: 0; font-size: 2rem; background: linear-gradient(135deg, #10B981, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{words:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown(f"""
        <div class='metric-card'>
            <p style='font-size: 2.5rem; margin: 0;'>⏱️</p>
            <p style='margin: 12px 0 6px 0; color: var(--text-tertiary); font-size: 0.9rem;'>Generated At</p>
            <h2 style='margin: 0; font-size: 1.2rem; background: linear-gradient(135deg, #F59E0B, #FBBF24); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{datetime.now().strftime("%H:%M")}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col4:
        st.markdown(f"""
        <div class='metric-card'>
            <p style='font-size: 2.5rem; margin: 0;'>✅</p>
            <p style='margin: 12px 0 6px 0; color: var(--text-tertiary); font-size: 0.9rem;'>Status</p>
            <h2 style='margin: 0; font-size: 1.3rem; color: #10B981;'>Complete</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Premium Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📰 Sources", "📋 Full Report", "🎯 Expert Critique", "📥 Export & Share"])
    
    # Tab 1: Sources
    with tab1:
        st.markdown("""
        <div style='padding: 20px 0;'>
            <h3 style='margin-bottom: 20px;'>🔍 Research Sources</h3>
            <p style='color: var(--text-tertiary); margin-bottom: 20px;'>
                Found <strong style='color: var(--accent-1);'>{}</strong> authoritative sources for this research
            </p>
        </div>
        """.format(len(results['urls'])), unsafe_allow_html=True)
        
        for idx, url in enumerate(results["urls"], 1):
            st.markdown(f"""
            <div class='url-card'>
                <div style='display: flex; justify-content: space-between; align-items: start;'>
                    <div style='flex: 1;'>
                        <p style='margin: 0 0 8px 0; color: var(--text-tertiary); font-size: 0.85rem; font-weight: 600;'>SOURCE {idx}</p>
                        <a href='{url}' target='_blank' style='color: var(--accent-1); text-decoration: none; word-break: break-all; transition: all 0.3s ease;' onmouseover="this.style.color='#00D9FF'" onmouseout="this.style.color='#0066FF'">
                            {url}
                        </a>
                    </div>
                    <a href='{url}' target='_blank' style='margin-left: 10px; color: var(--accent-1); text-decoration: none; font-size: 1.2rem;'>↗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tab 2: Full Report
    with tab2:
        st.markdown("""
        <div style='padding: 20px 0; margin-bottom: 20px;'>
            <h3 style='margin: 0 0 10px 0;'>📋 Comprehensive Analysis</h3>
            <p style='color: var(--text-tertiary); margin: 0; font-size: 0.95rem;'>
                Full investigative report with detailed findings and analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display report in a beautiful card
        st.markdown(f"""
        <div class='card' style='padding: 40px; line-height: 1.8;'>
            {results["report"]}
        </div>
        """, unsafe_allow_html=True)
    
    # Tab 3: Critique
    with tab3:
        st.markdown("""
        <div style='padding: 20px 0; margin-bottom: 20px;'>
            <h3 style='margin: 0 0 10px 0;'>🎯 Expert Review</h3>
            <p style='color: var(--text-tertiary); margin: 0; font-size: 0.95rem;'>
                Senior academic assessment of report quality and depth
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='card' style='padding: 40px; line-height: 1.8;'>
            {results["critique"]}
        </div>
        """, unsafe_allow_html=True)
    
    # Tab 4: Export
    with tab4:
        st.markdown("""
        <div style='padding: 20px 0; margin-bottom: 20px;'>
            <h3 style='margin: 0 0 10px 0;'>📥 Download & Share</h3>
            <p style='color: var(--text-tertiary); margin: 0; font-size: 0.95rem;'>
                Export your research in multiple formats
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Download Options
        export_col1, export_col2, export_col3 = st.columns(3, gap="medium")
        
        # TXT Export
        with export_col1:
            full_report = f"""
{'='*100}
RESEARCH REPORT
{'='*100}

TOPIC: {results['topic']}
GENERATED: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{'='*100}
SOURCES ({len(results['urls'])})
{'='*100}

{chr(10).join([f'{i}. {url}' for i, url in enumerate(results['urls'], 1)])}

{'='*100}
COMPREHENSIVE ANALYSIS
{'='*100}

{results["report"]}

{'='*100}
EXPERT CRITIQUE
{'='*100}

{results["critique"]}

{'='*100}
END OF REPORT
            """
            
            st.download_button(
                label="📄 Text Report",
                data=full_report,
                file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="txt_export"
            )
        
        # JSON Export
        with export_col2:
            json_data = json.dumps({
                "topic": results['topic'],
                "generated": datetime.now().isoformat(),
                "urls": results['urls'],
                "report": results['report'],
                "critique": results['critique']
            }, indent=2)
            
            st.download_button(
                label="📊 JSON Data",
                data=json_data,
                file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
                key="json_export"
            )
        
        # Markdown Export
        with export_col3:
            markdown_report = f"""# {results['topic']}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📰 Sources

{chr(10).join([f'- [{i}]({url})' for i, url in enumerate(results['urls'], 1)])}

## 📋 Analysis

{results['report']}

## 🎯 Expert Assessment

{results['critique']}
"""
            
            st.download_button(
                label="📝 Markdown",
                data=markdown_report,
                file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
                key="md_export"
            )
        
        st.divider()
        
        # Share message
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0, 217, 255, 0.1), rgba(157, 0, 255, 0.05)); border: 1px solid rgba(0, 217, 255, 0.2); border-radius: 16px; padding: 20px; text-align: center;'>
            <p style='margin: 0; color: var(--accent-1); font-weight: 700;'>✨ Ready to Share</p>
            <p style='margin: 10px 0 0 0; color: var(--text-secondary); font-size: 0.9rem;'>
                Download and share your research findings with colleagues and stakeholders
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # New Research Button
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Start New Research", use_container_width=True, key="new_research"):
            st.session_state.research_results = None
            st.rerun()

# =========================================
# PREMIUM FOOTER
# =========================================

st.divider()

st.markdown("""
<div style='text-align: center; padding: 40px 20px; background: linear-gradient(180deg, rgba(0, 217, 255, 0.05) 0%, transparent 100%); border-top: 1px solid rgba(0, 217, 255, 0.1); border-radius: 20px; margin-top: 20px;'>
    <h3 style='margin: 0; background: linear-gradient(135deg, #00D9FF, #9D00FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Research AI</h3>
    <p style='color: var(--text-tertiary); margin: 10px 0 0 0; font-size: 0.95rem;'>
        Next-Generation Investigative Research Platform
    </p>
    <p style='color: var(--text-tertiary); margin: 12px 0 0 0; font-size: 0.85rem;'>
        Powered by Groq AI • LangChain • Tavily Search API
    </p>
    <p style='color: #7A8BA8; margin: 12px 0 0 0; font-size: 0.8rem;'>
        Built with ✨ for advanced research analysis
    </p>
</div>
""", unsafe_allow_html=True)
