import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from PIL import Image, ImageOps
import io
import copy
import base64
import os
import inspect
# import textwrap

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="S-Box Prime Lab",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- NAVBAR IMPLEMENTATION ---
@st.cache_data
def get_nav_logo(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

try:
    logo_b64 = get_nav_logo("logo_unnes.png")
    logo_tag = f'<img src="data:image/png;base64,{logo_b64}" class="nav-logo-box">'
except:
    logo_tag = ""

st.markdown(f"""
    <div id="custom-navbar">
        <div class="nav-left-content">
            {logo_tag}
            <div class="nav-brand-text">
                <div class="nav-brand-main">S-Box Research Lab</div>
                <div class="nav-brand-sub">UNNES Informatics Engineering</div>
            </div>
        </div>
        <div class="nav-right-content">
            <div class="nav-status-box">
                SYSTEM_ID: <span style="color:white;">K44_CORE</span> 
                <span class="nav-status-dot">●</span> 
                <span style="color:#00f2fe;">ACTIVE</span>
            </div>
        </div>
    </div>

    <script>
    var lastScroll = 0;
    const nav = document.getElementById('custom-navbar');
    // Mencari kontainer scroll utama di Streamlit
    const scrollTarget = window.parent.document.querySelector('.main');

    scrollTarget.addEventListener('scroll', function() {{
        var currentScroll = scrollTarget.scrollTop;
        
        if (currentScroll > lastScroll && currentScroll > 150) {{
            // Scroll Down - Sembunyikan dengan slide up [cite: 1, 4]
            nav.style.transform = "translateY(-100%)";
        }} else {{
            // Scroll Up - Munculkan kembali [cite: 1, 4]
            nav.style.transform = "translateY(0)";
        }}
        lastScroll = currentScroll;
    }}, {{ passive: true }});
    </script>
""", unsafe_allow_html=True)

# --- 2. ADVANCED CSS STYLING WITH ANIMATIONS ---
st.markdown("""
<style>
    /* ================= IMPORT FONTS ================= */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;500;600;700&family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400&display=swap');

    /* ================= ANIMATIONS ================= */
    @keyframes fadeInUp { from { opacity: 0; transform: translate3d(0, 30px, 0); } to { opacity: 1; transform: translate3d(0, 0, 0); } }
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-6px); } 100% { transform: translateY(0px); } }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }

    /* ================= GLOBAL STYLES ================= */
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }

    .stApp {
        background-color: #030305;
        background-image: 
            radial-gradient(at 20% 20%, hsla(253,16%,10%,1) 0, transparent 50%), 
            radial-gradient(at 80% 0%, hsla(225,39%,25%,1) 0, transparent 50%), 
            radial-gradient(at 50% 80%, hsla(339,49%,20%,1) 0, transparent 50%);
        font-family: 'Inter', sans-serif;
        background-attachment: fixed;
    }

    .main .block-container {
        animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
    }
    
    /* 1. MENGHAPUS PADDING BAWAH DARI CONTAINER UTAMA */
    /* Target class 'block-container' yang terlihat di inspect element */
    .block-container, div[data-testid="stMainBlockContainer"] {
        padding-bottom: 0px !important;
        padding-left: 3rem !important; /* Opsional: sesuaikan margin kiri */
        padding-right: 3rem !important; /* Opsional: sesuaikan margin kanan */
        max-width: 100vw !important; /* Agar lebar maksimal mengikuti layar */
    }

    /* 2. MENGHILANGKAN FOOTER BAWAAN STREAMLIT */
    /* Ini penting agar tidak ada 'hantu' elemen di bawah */
    footer, header {
        visibility: hidden;
        display: none !important;
        height: 0px !important;
    }
    

    /* 4. PASTIKAN FOOTER KAMU TIDAK PUNYA MARGIN LUAR */
    .footer-container {
        margin-bottom: 0px !important;
        padding-bottom: 20px; /* Padding dalam footer saja */
    }

    /* TYPOGRAPHY */
    h1, h2, h3, .tech-font {
        font-family: 'Rajdhani', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    h1 {
        background: linear-gradient(120deg, #ffffff 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem !important;
        text-shadow: 0 0 25px rgba(79, 172, 254, 0.4);
    }
    
    /* ================= NAVBAR STYLES ================= */
    #custom-navbar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 65px;
        background: rgba(3, 3, 5, 0.25); /* Deep dark semi-transparent  */
        backdrop-filter: blur(15px); /* Strong glassmorphism  */
        -webkit-backdrop-filter: blur(15px);
        border-bottom: 1px solid rgba(0, 242, 254, 0.2); /* Subtle Cyan Glow  */
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 40px;
        z-index: 10000;
        transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1); /* Smooth Slide  */
    }

    .nav-left-content {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .nav-logo-box {
        height: 32px;
        filter: drop-shadow(0 0 5px rgba(0, 242, 254, 0.3)); /* Logo Glow  */
    }

    .nav-brand-text {
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .nav-brand-main {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.1rem;
        line-height: 1;
    }

    .nav-brand-sub {
        color: #00f2fe; /* Cyber Cyan  */
        font-size: 0.7rem;
        font-weight: 500;
        margin-top: 2px;
    }

    .nav-status-box {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: #8899ac;
        background: rgba(255, 255, 255, 0.05);
        padding: 5px 12px;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .nav-status-dot {
        color: #00f2fe;
        text-shadow: 0 0 8px #00f2fe;
        animation: blink 2s infinite;
    }

    /* Adjust main content padding to prevent overlap  */
    .main .block-container {
        padding-top: 85px !important;
    }

    /* ================= COMPONENT: RESEARCH PANEL (CARD STYLE) ================= */
    .research-panel {
        background-color: #18181b; /* Darker grey background */
        border: 1px solid #333;
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 40px;
    }

    .panel-header {
        border-bottom: 1px solid #333;
        padding-bottom: 15px;
        margin-bottom: 25px;
    }

    .panel-title {
        color: #fff;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
    }

    .panel-subtitle {
        color: #8899ac;
        font-size: 0.9rem;
        margin-top: 5px;
    }

    .sub-section-box {
        background: #0f0f12;
        border: 1px solid #2d2d33;
        border-radius: 8px;
        padding: 15px;
        margin-top: 10px;
    }

    /* ================= EXISTING COMPONENT STYLES ================= */
    
    /* KPI CARDS */
    .kpi-card {
        background: rgba(20, 20, 30, 0.5);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 24px;
        transition: all 0.4s;
        animation: float 6s ease-in-out infinite;
        overflow: hidden;
    }
    .kpi-card:hover {
        transform: translateY(-12px) scale(1.03);
        border-color: rgba(0, 242, 254, 0.4);
        box-shadow: 0 15px 40px rgba(0, 242, 254, 0.2);
    }
    .kpi-title { color: #8899ac; font-size: 0.9rem; font-family: 'Rajdhani'; font-weight: 600; text-transform: uppercase; }
    .kpi-value { color: #fff; font-size: 2.8rem; font-weight: 700; font-family: 'Rajdhani'; text-shadow: 0 0 15px rgba(255, 255, 255, 0.2); }
    .kpi-footer { font-size: 0.8rem; margin-top: 12px; display: flex; align-items: center; gap: 6px; opacity: 0.8; }
    .status-ok { color: #00f2fe; } .status-warn { color: #ff0055; }

    /* MATRIX BITS */
    .matrix-box {
        font-family: 'JetBrains Mono', monospace;
        background: transparent; 
        padding: 5px;
    }
    
    .bit-1, .bit-0 { display: inline-block; transition: all 0.2s; cursor: crosshair; padding: 0 2px; }
    .bit-1 { color: #00f2fe; font-weight: bold; text-shadow: 0 0 4px #00f2fe; }
    .bit-0 { color: #444; }
    .bit-1:hover, .bit-0:hover { transform: scale(1.4); color: #ffffff; text-shadow: 0 0 8px #ffffff, 0 0 15px #00f2fe; z-index: 10; }
    .row-label { color: #666; margin-right: 15px; font-size: 0.8rem; }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(90deg, #2D5BFF, #1E40BF);
        color: white;
        border: none;
        height: 50px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 2px;
        border-radius: 6px;
        transition: all 0.3s;
        text-transform: uppercase;
        width: 100%;
        box-shadow: 0 5px 15px rgba(45, 91, 255, 0.3);
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(45, 91, 255, 0.6); color: #fff; }

    /* TERMINAL */
    .terminal-line { opacity: 0; animation: fadeInUp 0.5s ease forwards; }
    .anim-delay-1 { animation-delay: 0.1s; }
    .anim-delay-2 { animation-delay: 0.3s; }
    .anim-delay-3 { animation-delay: 0.5s; }
    .anim-delay-4 { animation-delay: 0.7s; }
    .anim-delay-5 { animation-delay: 0.9s; }
    .anim-delay-6 { animation-delay: 1.1s; }
    
    .section-separator { height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent); margin: 60px 0 40px 0; }
    
    /* ================= HERO SECTION STYLES ================= */
    .hero-badge {
        background: rgba(255, 255, 255, 0.1);
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.8rem;
        letter-spacing: 2px;
        color: #ccc;
        display: inline-block;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .hero-title-main {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 4rem !important;
        font-weight: 700 !important;
        line-height: 1;
        margin-bottom: 10px;
        color: white;
    }

    .hero-subtitle-main {
        color: #8899ac;
        font-size: 1.2rem;
        max-width: 600px;
        margin-bottom: 30px;
    }

    .status-container {
        position: absolute;
        top: 20px;
        right: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.8rem;
        font-family: 'JetBrains Mono';
    }

    .hero-card-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-top: 25px;
    }

    .hero-metric-card {
        background: rgba(20, 20, 30, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        padding: 12px 15px;
        backdrop-filter: blur(12px);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 100px; 
        transition: all 0.3s ease;
    }

    .hero-metric-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(0, 242, 254, 0.3);
        transform: translateY(-3px);
    }

    .hero-metric-title {
        color: #8899ac;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.55rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0px;
    }

    .hero-metric-value {
        color: #ffffff;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.75rem;
        font-weight: 700;
        line-height: 1;
        margin: 8px 0;
        text-shadow: 0 0 15px rgba(255,255,255,0.1);
    }

    .hero-metric-footer {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #e0e0e0;
        font-size: 0.6rem;
        margin top: 2px;
    }

    .status-dot-teal {
        height: 7px;
        width: 7px;
        background-color: #00f2fe;
        border-radius: 50%;
        box-shadow: 0 0 8px #00f2fe;
    }
    
    /* ================= TEAM SECTION STYLES ================= */
    .team-container {
        display: flex;
        gap: 20px;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 40px;
    }

    .team-card {
        background: #000000;
        border-radius: 20px;
        width: 250px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .team-card:hover {
        transform: translateY(-10px);
        border-color: rgba(0, 242, 254, 0.5);
        box-shadow: 0 15px 40px rgba(0, 242, 254, 0.2);
    }

    .team-img-container {
        height: 280px;
        width: 100%;
        overflow: hidden;
    }

    .team-img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .team-info {
        padding: 20px;
        text-align: center;
        background: #000000;
    }

    .team-name {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 5px;
    }

    .team-desc {
        color: #888;
        font-size: 0.8rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* ================= PIPELINE SECTION STYLES ================= */
    .workflow-container {
        padding: 40px 20px;
        background: rgba(255, 255, 255, 0.01);
        border-radius: 20px;
    }

    .workflow-item {
        position: relative;
        padding-left: 45px;
        margin-bottom: 30px;
        border-left: 1px solid rgba(0, 242, 254, 0.2);
        animation: fadeInUp 0.8s ease backwards;
    }

    .workflow-item::before {
        content: '';
        position: absolute;
        left: -6px;
        top: 0;
        width: 11px;
        height: 11px;
        background: #00f2fe;
        border-radius: 50%;
        box-shadow: 0 0 15px #00f2fe;
    }

    .workflow-step-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #00f2fe;
        letter-spacing: 2px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .workflow-card {
        background: rgba(20, 20, 30, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        transition: 0.3s;
    }

    .workflow-card:hover {
        border-color: rgba(0, 242, 254, 0.4);
        background: rgba(255, 255, 255, 0.03);
        transform: translateX(10px);
    }
    
    .math-box {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 8px;
        padding: 12px;
        margin-top: 10px;
        border: 1px dashed rgba(0, 242, 254, 0.2);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #00f2fe;
    }
    .step-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .workflow-title {
        font-family: 'Rajdhani', sans-serif;
        color: #fff;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .workflow-desc {
        color: #8899ac;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .workflow-tag {
        display: inline-block;
        background: rgba(0, 242, 254, 0.1);
        color: #00f2fe;
        padding: 2px 10px;
        border-radius: 4px;
        font-size: 0.75rem;
        margin-top: 15px;
        font-family: 'JetBrains Mono';
        border: 1px solid rgba(0, 242, 254, 0.2);
    }
    
    /* ================= WORKFLOW SUMMARY & TAGS ================= */
    .wf-summary-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-top: 20px;
    }

    .wf-summary-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        transition: 0.3s;
    }

    .wf-summary-card:hover {
        border-color: #00f2fe;
        background: rgba(0, 242, 254, 0.02);
    }

    .wf-detail-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-top: 15px;
    }

    .wf-detail-card {
        background: rgba(10, 10, 15, 0.6);
        padding: 20px;
        border-radius: 12px;
        border-left: 3px solid #00f2fe;
    }

    .metric-pill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 15px;
    }

    .metric-pill {
        background: rgba(255, 255, 255, 0.05);
        color: #e0e0e0;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-family: 'JetBrains Mono', monospace;
    }
    
    .comparison-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background: rgba(20, 20, 30, 0.4);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .comparison-table th {
        background: rgba(0, 242, 254, 0.1);
        color: #00f2fe;
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        padding: 15px;
        text-align: left;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }
    .comparison-table td {
        padding: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        color: #e0e0e0;
        font-size: 0.9rem;
    }
    .comparison-table tr:hover {
        background: rgba(255, 255, 255, 0.02);
    }
    .highlight-k44 {
        color: #00f2fe;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-name {
        font-weight: 600;
        color: #fff;
    }
    
    /* ================= FOOTER STYLES ================= */
    [data-testid="stAppViewBlockContainer"] {
    padding-bottom: 0px !important;
    margin-bottom: 0px !important;
    }
    
    footer {
    display: none !important;
    }
    
    /* Menghilangkan gap di akhir blok vertikal Streamlit */
    div[data-testid="stVerticalBlock"] > div:last-child {
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }

    /* Memastikan elemen app tidak memiliki scrollbar horizontal akibat 100vw */
    .stApp {
        overflow-x: hidden;
    }

    .footer-container {
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        background: rgba(10, 10, 15, 0.98);
        border-top: 1px solid rgba(0, 242, 254, 0.2);
        padding: 60px 0 30px 0;
        margin-top: 100px;
        margin-bottom: 0px !important; /* Pastikan tidak ada margin bawah */
    }

    .footer-grid {
        display: grid;
        grid-template-columns: 1.5fr 1fr 1fr 1.2fr;
        gap: 30px;
    }

    .footer-brand-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: white;
        margin-bottom: 12px;
    }

    .footer-heading {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.9rem;
        font-weight: 700;
        color: #00f2fe;
        text-transform: uppercase;
        margin-bottom: 20px;
        letter-spacing: 2px;
    }

    .footer-link {
        display: block;
        color: #8899ac;
        text-decoration: none;
        font-size: 0.85rem;
        margin-bottom: 10px;
        transition: 0.3s;
    }

    .footer-link:hover {
        color: #00f2fe;
        padding-left: 5px;
    }

    .footer-bottom {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
        color: #52525b;
        font-size: 0.75rem;
    }
    .footer-content-wrapper {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 40px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MATH ENGINE ---
K44_MATRIX = [0x57, 0xAB, 0xD5, 0xEA, 0x75, 0xBA, 0x5D, 0xAE]
K43_MATRIX = [0xD5, 0xAB, 0x57, 0xEA, 0x75, 0xBA, 0x5D, 0xAE]
AES_MATRIX = [0xF1, 0xE3, 0xC7, 0x8F, 0x1F, 0x3E, 0x7C, 0xF8]

PRESETS = {
    "K44 (Optimal)": K44_MATRIX,
    "K43 (Variant)": K43_MATRIX,
    "AES (Standard)": AES_MATRIX,
    "Identity": [1, 2, 4, 8, 16, 32, 64, 128]
}

if 'current_matrix' not in st.session_state:
    st.session_state.current_matrix = K44_MATRIX.copy()
    st.session_state.matrix_name = "K44 (Optimal)"
if 'const_c' not in st.session_state:
    st.session_state.const_c = 0x63


# --- REPLACEMENT CODE FOR MATH ENGINE ---

def fwht(a):
    """Fast Walsh-Hadamard Transform (Vectorized for Speed)"""
    a = np.array(a, dtype=int)
    h = 1
    n = len(a)
    while h < n:
        temp = a.reshape((-1, 2, h))
        x = temp[:, 0, :].copy()
        y = temp[:, 1, :].copy()
        temp[:, 0, :] = x + y
        temp[:, 1, :] = x - y
        a = temp.reshape(-1)
        h *= 2
    return a

@st.cache_data
def calculate_metrics(sbox):
    sbox = np.array(sbox, dtype=int)
    size = 256
    metrics = {}
    
    # --- 1. NONLINEARITY (NL) & 8. ALGEBRAIC DEGREE (AD) ---
    nl_values = []
    max_deg = 0
    
    # Check all 255 non-zero linear combinations for robustness
    for b in range(1, 256):
        # f_b(x) = parity(b & S[x])
        val = sbox & b
        val ^= val >> 4
        val ^= val >> 2
        val ^= val >> 1
        val &= 1
        
        # NL Calculation
        f_walsh = 1 - 2 * val
        w = fwht(f_walsh)
        nl = (size - np.max(np.abs(w))) // 2
        nl_values.append(nl)
        
        # AD Calculation (Mobius Transform on 8 coordinate functions only)
        if (b & (b-1) == 0): # Check if b is power of 2 (coordinate function)
            anf = val.copy()
            h = 1
            while h < 256:
                temp = anf.reshape((-1, 2, h))
                temp[:, 1, :] ^= temp[:, 0, :]
                anf = temp.reshape(-1)
                h *= 2
            # Max weight of index with non-zero coeff
            idxs = np.nonzero(anf)[0]
            if len(idxs) > 0:
                wts = np.array([bin(x).count('1') for x in idxs])
                deg = np.max(wts)
                if deg > max_deg:
                    max_deg = deg

    metrics['nl_min'] = np.min(nl_values)
    metrics['nl_avg'] = np.mean(nl_values)
    metrics['ad'] = max_deg

    # --- 2. SAC ---
    sac_matrix = np.zeros((8, 8))
    for i in range(8):
        mask_in = 1 << i
        for j in range(8):
            mask_out = 1 << j
            diff = (sbox ^ sbox[np.arange(size) ^ mask_in]) & mask_out
            cnt = np.count_nonzero(diff)
            sac_matrix[i, j] = cnt / size
    metrics['sac_avg'] = np.mean(sac_matrix)
    metrics['sac_matrix'] = sac_matrix

    # --- 3. BIT INDEPENDENCE CRITERION (BIC) ---
    bic_nl_vals = []
    bic_sac_vals = []
    
    for i in range(8):
        for j in range(i+1, 8):
            combined_mask = (1 << i) | (1 << j)
            # BIC-NL: NL of f_i ^ f_j
            val = sbox & combined_mask
            val ^= val >> 4; val ^= val >> 2; val ^= val >> 1; val &= 1
            w = fwht(1 - 2 * val)
            bic_nl_vals.append((size - np.max(np.abs(w))) // 2)
            
            # BIC-SAC: Avg SAC of f_i ^ f_j
            pair_sac_sum = 0
            for k in range(8):
                diff_s = sbox ^ sbox[np.arange(size) ^ (1<<k)]
                bits_diff = diff_s & combined_mask
                p_diff = bits_diff
                p_diff ^= p_diff >> 4; p_diff ^= p_diff >> 2; p_diff &= 1
                pair_sac_sum += np.count_nonzero(p_diff) / size
            bic_sac_vals.append(pair_sac_sum / 8)
            
    metrics['bic_nl'] = np.min(bic_nl_vals)
    metrics['bic_sac'] = np.mean(bic_sac_vals)

    # --- 4. LAP ---
    # LAP = (128 - NL_min) / 256
    metrics['lap'] = (128 - metrics['nl_min']) / 256.0

    # --- 5. DIFFERENTIAL UNIFORMITY (DU) & DAP ---
    ddt = np.zeros((size, size), dtype=int)
    for dx in range(1, size):
        dy = sbox ^ sbox[np.arange(size) ^ dx]
        np.add.at(ddt[dx], dy, 1)
    
    metrics['du_max'] = int(np.max(ddt[1:]))
    metrics['dap'] = metrics['du_max'] / size
    metrics['ddt'] = ddt

    # --- 6. CORRELATION IMMUNITY (CI) ---
    min_ci_found = 8
    wts = np.array([bin(x).count('1') for x in range(size)])
    
    for b in range(1, 256):
        val = sbox & b
        val ^= val >> 4; val ^= val >> 2; val ^= val >> 1; val &= 1
        w = fwht(1 - 2 * val)
        idxs = np.nonzero(w)[0]
        if len(idxs) > 0:
            current_min_wt = np.min(wts[idxs])
            # CI is order t such that W(a)=0 for 1 <= wt(a) <= t
            ci_b = max(0, current_min_wt - 1)
            if ci_b < min_ci_found:
                min_ci_found = ci_b
    metrics['ci'] = min_ci_found

    # --- 7. TRANSPARENCY ORDER (TO) ---
    beta_term = 8 - 2 * wts
    sum_abs_walsh = np.zeros(size)
    for a in range(1, size):
        d_a = sbox ^ sbox[np.arange(size) ^ a]
        counts = np.bincount(d_a, minlength=size)
        w_diff = fwht(counts) # Walsh of derivative histogram
        sum_abs_walsh += np.abs(w_diff)
        
    coeff = 1.0 / (size*size - size)
    metrics['to'] = np.max(beta_term - coeff * sum_abs_walsh)

    # --- 8. FIXED POINTS ---
    metrics['fixed_points'] = np.sum(sbox == np.arange(size))
    
    return metrics


def gf_inverse(byte):
    if byte == 0:
        return 0
    p, t, newt = 0x11B, 0, 1
    r, newr = 0x11B, byte
    while newr != 0:
        if newr != 0:
            deg_r = r.bit_length() - 1
            deg_newr = newr.bit_length() - 1
            while deg_r >= deg_newr:
                shift = deg_r - deg_newr
                r ^= (newr << shift)
                t ^= (newt << shift)
                deg_r = r.bit_length() - 1
        r, newr = newr, r
        t, newt = newt, t
    return t


INVERSE_TABLE = [gf_inverse(x) for x in range(256)]


def generate_sbox_data(matrix, c):
    res = []
    for x in range(256):
        inv = INVERSE_TABLE[x]
        val = 0
        for i in range(8):
            row_val = matrix[i]
            temp = inv & row_val
            parity = bin(temp).count('1') % 2
            c_bit = (c >> i) & 1
            if parity ^ c_bit:
                val |= (1 << i)
        res.append(val)
    return res

# --- 4. UI HELPER FUNCTIONS ---


def render_kpi(title, value, footer, status="ok"):
    st.markdown(f"""
    <div class="kpi-card" style="animation: fadeInUp 0.6s ease backwards;">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-footer"><span class="{'status-ok' if status == 'ok' else 'status-warn'}" style="font-size:1.2rem;">●</span> {footer}</div>
    </div>
    """, unsafe_allow_html=True)


def render_heatmap(data, title, xlabel, ylabel, cmap="magma"):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(data, ax=ax, cmap=cmap, cbar=False)
    ax.set_title(title, color='white', fontsize=12, pad=10,
                 fontfamily='Rajdhani', fontweight='bold')
    ax.set_xlabel(xlabel, color='#888', fontsize=9, fontfamily='Inter')
    ax.set_ylabel(ylabel, color='#888', fontsize=9, fontfamily='Inter')
    ax.tick_params(colors='#888', labelsize=8)
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    for _, spine in ax.spines.items():
        spine.set_color('#333')
    return fig

# --- 5. MAIN PAGE LAYOUT ---

# Layout Utama Hero: Logo di kiri, Teks di kanan
hero_col1, hero_col2 = st.columns([1.19, 2.2], gap="large")

with hero_col1:
    try:
        logo = Image.open("logo_unnes.png")
        st.image(logo, use_container_width=True)
    except FileNotFoundError:
        st.error("File logo_unnes.png tidak ditemukan.")

with hero_col2:
    st.markdown('<div class="hero-badge">● UNIVERSITAS NEGERI SEMARANG</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title-main">AES S-Box<br>Research Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("""
        <p class="hero-subtitle-main">
            Explore AES S-box variants, evaluate their cryptographic strength, 
            and visualize results with intuitive tools.
        </p>
    """, unsafe_allow_html=True)

    # Grid 4 Card KPI (Menggantikan Buttons)
    st.markdown("""
    <div class="hero-card-container">
        <div class="hero-metric-card">
            <div class="hero-metric-title">Nonlinearity</div>
            <div class="hero-metric-value">112</div>
            <div class="hero-metric-footer">
                <span class="status-dot-teal"></span> Optimal (AES Standard)
            </div>
        </div>
        <div class="hero-metric-card">
            <div class="hero-metric-title">Diff. Uniformity</div>
            <div class="hero-metric-value">4</div>
            <div class="hero-metric-footer">
                <span class="status-dot-teal"></span> Resistant to Attacks
            </div>
        </div>
        <div class="hero-metric-card">
            <div class="hero-metric-title">Avalanche (SAC)</div>
            <div class="hero-metric-value">0.50</div>
            <div class="hero-metric-footer">
                <span class="status-dot-teal"></span> Ideal Bit Diffusion
            </div>
        </div>
        <div class="hero-metric-card">
            <div class="hero-metric-title">Fixed Points</div>
            <div class="hero-metric-value">0</div>
            <div class="hero-metric-footer">
                <span class="status-dot-teal"></span> No Self-Mappings
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

# === SECTION: RESEARCH TEAM ===
st.markdown("""
<div style='text-align: center; margin-top: 30px; width: 100%;'>
    <h2 class="tech-font" style='text-align: center; margin-bottom: 0px;'>LINE-UP TIM</h2>
    <p style='color: #8899ac; font-size: 1rem; text-align: center; margin-bottom: 60px;'>
        Cita-cita menjadi developer handal namun enggan berlatih dan membuat portfolio
    </p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def get_base64_image(image_path):
    try:
        with Image.open(image_path) as img:
            img = ImageOps.exif_transpose(img)
            
            img = img.convert("RGB")
            
            target_size = (600, 800)
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=90, optimize=True)
            
            return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        return ""

team_members = [
    {"name": "Satriya Cahyo Wisely", "file": "Wisely.JPG", "nim": "2304130053", "desc": "Pria Dingin from Wonosobo"},
    {"name": "M. Zuhrifar Roihan", "file": "Roihan.JPG", "nim": "2304130055", "desc": "Pria Tamvan from Tegal"},
    {"name": "M. Khayri Faadhil", "file": "Khayri.JPG", "nim": "2304130062", "desc": "Pria Nonchalant from Boyolali"},
    {"name": "Zhahiran Abyan Muhsin", "file": "Byan.JPG", "nim": "2304130065", "desc": "Pria Kalcer from Bandung"},    
]

# Render Team Cards
cols = st.columns(4)
for i, member in enumerate(team_members):
    with cols[i]:
        img_base64 = get_base64_image(member["file"])
        img_src = f"data:image/jpeg;base64,{img_base64}" if img_base64 else ""
        
        st.markdown(f"""
        <div class="team-card">
            <div class="team-img-container">
                <img src="{img_src}" style="width:100%; height:100%; object-fit:cover;">
            </div>
            <div class="team-info">
                <div class="team-name">{member['name']}</div>
                <div class="team-desc">{member['desc']} | {member['nim']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

# === SECTION: LABORATORY (RESTRUCTURED) ===
st.markdown("<div style='text-align: center; margin-bottom: 40px; animation: fadeInUp 0.8s ease;'><h2>🧪 EXPERIMENTAL LABORATORY</h2></div>", unsafe_allow_html=True)

# RESEARCH PANEL (MATRIX)
with st.container():

    st.markdown("""
        <div class="panel-header">
            <div class="panel-title">Research Parameters</div>
            <div class="panel-subtitle">Adjust S-box generation parameters and constants</div>
        </div>
    """, unsafe_allow_html=True)

    c_mat, c_ctrl = st.columns([1.6, 1], gap="large")

    with c_mat:
        st.markdown("<div style='color:#bbb; font-weight:600; font-size:0.9rem; margin-bottom:5px;'>AFFINE TRANSFORMATION MATRIX</div>", unsafe_allow_html=True)
        preset_name = st.selectbox("Select Configuration", list(
            PRESETS.keys()), label_visibility="collapsed")
        if preset_name != st.session_state.matrix_name:
            st.session_state.current_matrix = PRESETS[preset_name].copy()
            st.session_state.matrix_name = preset_name
            st.rerun()

        desc_text = "Best Performer. NL=112, SAC=0.50073, BIC-NL=112" if "K44" in preset_name else "Alternative configuration."
        st.caption(f"ℹ️ {desc_text}")

        st.markdown("<div style='margin-top:20px; color:#bbb; font-weight:600; font-size:0.9rem; margin-bottom:5px;'>CURRENT MATRIX (BIT EDITOR)</div>", unsafe_allow_html=True)
        st.markdown('<div class="sub-section-box">', unsafe_allow_html=True)
        html = "<div class='matrix-box'>"
        for i, val in enumerate(st.session_state.current_matrix):
            bin_str = f"{val:08b}"
            bits_html = "".join(
                [f"<span class='{'bit-1' if b == '1' else 'bit-0'}'>{b}</span>" for b in bin_str])
            html += f"<div style='margin-bottom:5px; display: flex; justify-content: space-between;'><span class='row-label'>R{i}</span> <div>{bits_html}</div> <span style='color:#666; font-family: JetBrains Mono;'>0x{val:02X}</span></div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_ctrl:
        st.markdown(
            "<div style='color:#bbb; font-weight:600; font-size:0.9rem; margin-bottom:5px;'>CONSTANT VECTOR (C)</div>", unsafe_allow_html=True)
        new_c = st.text_input(
            "Hex Value", value=f"{st.session_state.const_c:02X}", label_visibility="collapsed")
        try:
            st.session_state.const_c = int(new_c, 16)
        except:
            pass
        st.caption(
            f"Hex/Decimal: 0x{st.session_state.const_c:02X} ({st.session_state.const_c})")

        st.markdown("<div style='margin-top:25px; color:#bbb; font-weight:600; font-size:0.9rem; margin-bottom:5px;'>ACTIVE PARAMETERS</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: #888; line-height: 1.6;">
            MATRIX: <span style="color:#eee">{st.session_state.matrix_name}</span><br>
            CONST: <span style="color:#eee">0x{st.session_state.const_c:02X}</span><br>
            EQ: <span style="color:#00f2fe">S(x) = M × x^(-1) ⊕ C</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 30px;'></div>",
                    unsafe_allow_html=True)
        if st.button("INITIATE SEQUENCE"):
            with st.spinner("PROCESSING..."):
                time.sleep(0.8)
                st.session_state.run_analysis = True

    st.markdown('</div>', unsafe_allow_html=True)

# RESULTS AREA
if st.session_state.get('run_analysis'):
    # 1. Generate Data & Metrics for Research S-Box
    custom_sbox = generate_sbox_data(st.session_state.current_matrix, st.session_state.const_c)
    metrics = calculate_metrics(custom_sbox)

    # 2. Generate Data & Metrics for AES Standard (Reference)
    #    Kita hitung on-the-fly agar adil menggunakan math engine yang sama
    aes_sbox_ref = generate_sbox_data(AES_MATRIX, 0x63)
    aes_metrics = calculate_metrics(aes_sbox_ref)

    st.markdown("<div style='animation: fadeInUp 0.8s ease;'>", unsafe_allow_html=True)
    
    # --- TABS LAYOUT ---
    t1, t2, t3 = st.tabs(["BENCHMARK TABLE", "VISUALIZATION (SAC/DDT)", "S-BOX COMPARISON"])

    # --- TAB 1: BENCHMARK TABLE (Styled like original) ---
    with t1:
        st.markdown("""
        <style>
            table { width: 100%; border-collapse: separate; border-spacing: 0 12px; }
            th { text-align: left; color: #8899ac; border-bottom: 1px solid #333; padding: 15px; font-family: 'Rajdhani'; letter-spacing: 1px; text-transform: uppercase; }
            td { background: rgba(255,255,255,0.03); padding: 18px 15px; color: #eee; font-family: 'Inter'; border-top: 1px solid #222; border-bottom: 1px solid #222; transition: all 0.3s; }
            tr:hover td { background: rgba(255,255,255,0.06); transform: scale(1.01); }
            td:first-child { border-top-left-radius: 10px; border-bottom-left-radius: 10px; border-left: 1px solid #222; font-weight: 600; color: #fff; }
            td:last-child { border-top-right-radius: 10px; border-bottom-right-radius: 10px; border-right: 1px solid #222; }
            .winner { color: #00f2fe; font-weight: bold; font-family: 'JetBrains Mono'; }
            .loser { color: #888; font-family: 'JetBrains Mono'; }
            .equal { color: #e0e0e0; font-family: 'JetBrains Mono'; }
            .metric-val { font-family: 'JetBrains Mono', monospace; font-size: 1.0rem; }
        </style>
        """, unsafe_allow_html=True)

        # Helper untuk menentukan pemenang visual
        def get_comp_html(val_research, val_aes, goal='max'):
            # Format angka
            v_res_str = f"{val_research:.4f}" if isinstance(val_research, float) else str(val_research)
            v_aes_str = f"{val_aes:.4f}" if isinstance(val_aes, float) else str(val_aes)

            # Logika Pemenang
            is_winner = False
            if goal == 'max':
                if val_research > val_aes: is_winner = True
            elif goal == 'min':
                if val_research < val_aes: is_winner = True
            elif goal == 'target_0.5':
                if abs(val_research - 0.5) < abs(val_aes - 0.5): is_winner = True

            # Return HTML column content
            if val_research == val_aes:
                return f'<td class="metric-val equal">{v_res_str}</td><td class="metric-val equal">{v_aes_str}</td><td><span class="hero-badge" style="color:#aaa; border-color:#444;">EQUAL</span></td>'
            elif is_winner:
                return f'<td class="metric-val winner">{v_res_str}</td><td class="metric-val loser">{v_aes_str}</td><td><span class="hero-badge" style="color:#00f2fe; border-color:#00f2fe;">RESEARCH (K44)</span></td>'
            else:
                return f'<td class="metric-val loser">{v_res_str}</td><td class="metric-val winner">{v_aes_str}</td><td><span class="hero-badge" style="color:#888; border-color:#444;">AES STANDARD</span></td>'

        # Generate Table Rows
        row_nl = get_comp_html(metrics['nl_min'], aes_metrics['nl_min'], 'max')
        row_du = get_comp_html(metrics['du_max'], aes_metrics['du_max'], 'min')
        row_sac = get_comp_html(metrics['sac_avg'], aes_metrics['sac_avg'], 'target_0.5')
        row_bic_nl = get_comp_html(metrics['bic_nl'], aes_metrics['bic_nl'], 'max')
        row_lap = get_comp_html(metrics['lap'], aes_metrics['lap'], 'min')
        row_dap = get_comp_html(metrics['dap'], aes_metrics['dap'], 'min')
        row_ad = get_comp_html(metrics['ad'], aes_metrics['ad'], 'max')
        row_to = get_comp_html(metrics['to'], aes_metrics['to'], 'min') # Lower TO is better against DPA
        row_ci = get_comp_html(metrics['ci'], aes_metrics['ci'], 'max')
        row_fp = get_comp_html(metrics['fixed_points'], aes_metrics['fixed_points'], 'min')

        st.markdown(f"""
        <table>
            <thead>
                <tr>
                    <th style="width:25%;">METRIC PARAMETER</th>
                    <th style="width:25%;">RESEARCH RESULT</th>
                    <th style="width:25%;">AES STANDARD</th>
                    <th style="width:25%;">PERFORMANCE VERDICT</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Nonlinearity (NL)</td>{row_nl}</tr>
                <tr><td>Differential Uniformity (DU)</td>{row_du}</tr>
                <tr><td>Strict Avalanche Crit. (SAC)</td>{row_sac}</tr>
                <tr><td>Bit Independence (BIC-NL)</td>{row_bic_nl}</tr>
                <tr><td>Linear Approx. Prob. (LAP)</td>{row_lap}</tr>
                <tr><td>Diff. Approx. Prob. (DAP)</td>{row_dap}</tr>
                <tr><td>Algebraic Degree (AD)</td>{row_ad}</tr>
                <tr><td>Transparency Order (TO)</td>{row_to}</tr>
                <tr><td>Correlation Immunity (CI)</td>{row_ci}</tr>
                <tr><td>Fixed Points</td>{row_fp}</tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)
        
        st.caption("ℹ️ Verdict determined by: Maximize NL, Minimize DU, Minimize Fixed Points, SAC closest to 0.5.")

    # --- TAB 2: VISUALIZATION (Side by Side) ---
    with t2:
        st.info("Visual comparison between Research S-Box and AES Standard. Brighter colors indicate higher values.")
        
        # Row 1: SAC Matrix
        st.markdown("##### 1. Strict Avalanche Criterion (SAC) Matrix")
        c_viz1, c_viz2 = st.columns(2, gap="medium")
        with c_viz1:
             st.markdown("<div style='background: rgba(255,255,255,0.02); padding: 15px; border-radius: 12px;'>", unsafe_allow_html=True)
             st.pyplot(render_heatmap(metrics['sac_matrix'], "Research S-Box (SAC)", "Output Bit", "Input Bit", "icefire"))
             st.markdown("</div>", unsafe_allow_html=True)
        with c_viz2:
             st.markdown("<div style='background: rgba(255,255,255,0.02); padding: 15px; border-radius: 12px;'>", unsafe_allow_html=True)
             st.pyplot(render_heatmap(aes_metrics['sac_matrix'], "AES Standard (SAC)", "Output Bit", "Input Bit", "icefire"))
             st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Row 2: DDT
        st.markdown("##### 2. Difference Distribution Table (DDT)")
        c_viz3, c_viz4 = st.columns(2, gap="medium")
        with c_viz3:
             st.markdown("<div style='background: rgba(255,255,255,0.02); padding: 15px; border-radius: 12px;'>", unsafe_allow_html=True)
             st.pyplot(render_heatmap(metrics['ddt'], "Research S-Box (DDT)", "Output Diff", "Input Diff", "mako"))
             st.markdown("</div>", unsafe_allow_html=True)
        with c_viz4:
             st.markdown("<div style='background: rgba(255,255,255,0.02); padding: 15px; border-radius: 12px;'>", unsafe_allow_html=True)
             st.pyplot(render_heatmap(aes_metrics['ddt'], "AES Standard (DDT)", "Output Diff", "Input Diff", "mako"))
             st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 3: S-BOX COMPARISON (Updated with Decimal Option) ---
    # --- TAB 3: S-BOX COMPARISON (Dengan Tombol Cyberpunk) ---
    with t3:
        # 1. INJEKSI CSS KHUSUS UNTUK RADIO BUTTON
        # CSS ini mengubah radio button horizontal menjadi tampilan "Tab/Pill"
        st.markdown("""
        <style>
            /* Container Radio Group */
            div[role="radiogroup"][aria-orientation="horizontal"] {
                background-color: #0f0f12;
                padding: 4px;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                display: inline-flex;
                gap: 8px;
            }
            
            /* Sembunyikan bulatan radio asli */
            div[role="radiogroup"][aria-orientation="horizontal"] label > div:first-child {
                display: none !important;
            }
            
            /* Style Label (Tombol) - Default State */
            div[role="radiogroup"][aria-orientation="horizontal"] label {
                background-color: transparent;
                padding: 8px 16px;
                border-radius: 6px;
                border: 1px solid transparent;
                transition: all 0.3s ease;
                cursor: pointer;
                color: #8899ac !important;
                font-family: 'Rajdhani', sans-serif;
                font-weight: 600;
                letter-spacing: 1px;
                font-size: 0.9rem;
                margin: 0 !important;
            }

            /* Hover State */
            div[role="radiogroup"][aria-orientation="horizontal"] label:hover {
                border-color: rgba(0, 242, 254, 0.3);
                color: #fff !important;
            }

            /* Active/Checked State (Menggunakan selector :has untuk mendeteksi pilihan) */
            div[role="radiogroup"][aria-orientation="horizontal"] label:has(input:checked) {
                background: rgba(0, 242, 254, 0.15);
                border-color: #00f2fe;
                color: #00f2fe !important;
                box-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
            }
            
            /* Fallback untuk teks di dalam label */
            div[role="radiogroup"] label p {
                font-weight: 600;
                margin-bottom: 0px;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("#### S-BOX LOOKUP TABLE COMPARISON")
        
        # 2. TOMBOL PILIHAN (Diposisikan di kanan atas tabel)
        c_head, c_btn = st.columns([2, 1])
        with c_head:
             st.caption("Bandingkan nilai byte antara S-Box hasil riset dengan standar AES dalam format Hex atau Decimal.")
        with c_btn:
            # Radio button ini akan otomatis terkena style CSS di atas
            num_format = st.radio(
                "Format Angka", 
                ["HEXADECIMAL", "DECIMAL"], 
                horizontal=True,
                label_visibility="collapsed",
                key="tab3_format_toggle"
            )
            
        hex_labels = [f"{i:X}" for i in range(16)]
        
        col_res, col_aes = st.columns(2, gap="large")
        
        # 3. LOGIKA FORMAT DATA
        if num_format == "HEXADECIMAL":
            # Format Hexadecimal (String, e.g., '99', 'F1')
            data_res = np.array([f"{x:02X}" for x in custom_sbox]).reshape(16, 16)
            data_aes = np.array([f"{x:02X}" for x in aes_sbox_ref]).reshape(16, 16)
            fmt_label = "HEX (16)"
        else:
            # Format Decimal (Integer, e.g., 153, 241)
            data_res = np.array(custom_sbox).reshape(16, 16)
            data_aes = np.array(aes_sbox_ref).reshape(16, 16)
            fmt_label = "DEC (10)"
        
        # 4. TAMPILAN TABEL
        with col_res:
            st.markdown(f"**K44 ({fmt_label})**")
            df_sbox = pd.DataFrame(data_res, columns=hex_labels, index=hex_labels)
            st.dataframe(df_sbox, use_container_width=True, height=450)
            
        with col_aes:
            st.markdown(f"**AES Standard ({fmt_label})**")
            df_aes = pd.DataFrame(data_aes, columns=hex_labels, index=hex_labels)
            st.dataframe(df_aes, use_container_width=True, height=450)

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center; margin-top:80px; color:#666; animation: fadeInUp 0.8s ease 0.4s backwards;">
        <h3 style="color:#888;">⚠ AWAITING INPUT SEQUENCE</h3>
        <p>Please select parameters above and click <b style="color:#00f2fe;">'INITIATE SEQUENCE'</b> to begin analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
# === SECTION: RESEARCH WORKFLOW (WITH MATH DETAILS) ===
st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; margin-bottom: 50px;'><h2 class='tech-font'>RESEARCH WORKFLOW</h2></div>", unsafe_allow_html=True)

# PENTING: Jangan beri spasi di awal baris dalam triple quotes di bawah ini
workflow_content = """
<div class="workflow-container">

<div class="workflow-item">
<div class="workflow-step-num">STEP 01 // SEARCH SPACE</div>
<div class="workflow-card">
<div class="workflow-title">Eksplorasi Matriks Affine 8×8</div>
<div class="workflow-desc">Menentukan matriks biner bisektif dari ruang pencarian $2^{64}$ kombinasi bit.</div>
<div class="math-box">Space Size = 2^(8 &times; 8) = 18,446,744,073,709,551,616</div>
</div>
</div>

<div class="workflow-item">
<div class="workflow-step-num">STEP 02 // GF(2⁸) INVERSION</div>
<div class="workflow-desc" style="color:#fff; font-weight:bold; margin-bottom:10px;">Transformasi Inverse & Polinomial</div>
<div class="workflow-card">
<div class="workflow-desc">Menghitung multiplicative inverse pada Galois Field $GF(2^8)$ menggunakan polinomial irreducible $x^8 + x^4 + x^3 + x + 1$ (0x11B).</div>
<div class="math-box">S(x) = M &times; x^{-1} &oplus; C</div>
</div>
</div>

<div class="workflow-item">
<div class="workflow-step-num">STEP 03 // CANDIDATE GENERATION</div>
<div class="workflow-card">
<div class="workflow-title">Pembentukan Tabel S-Box</div>
<div class="workflow-desc">Hasil pemetaan matriks $M$ dan konstanta $C$ menghasilkan 256 nilai unik dalam bentuk tabel lookup[cite: 29].</div>
<div class="workflow-tag">Total Candidates: 2⁶⁴ S-Boxes</div>
</div>
</div>

<div class="workflow-item">
<div class="workflow-step-num">STEP 04 // FILTERING</div>
<div class="workflow-card">
<div class="workflow-title">Seleksi Balance & Bijective</div>
<div class="workflow-desc">Hanya kandidat yang lolos uji keseimbangan bit (128 nol & 128 satu) dan pemetaan satu-ke-satu (0-255) yang dipertahankan[cite: 30, 43, 44].</div>
<div class="math-box">&sum; bits = 128 | Unique Values = {0...255}</div>
</div>
</div>

<div class="workflow-item">
<div class="workflow-step-num">STEP 05 // SECURITY SUITE</div>
<div class="workflow-card">
<div class="workflow-title">Analisis 10 Metrik Kriptografi</div>
<div class="workflow-desc">Pengujian otomatis terhadap Nonlinearity (NL), SAC, DU, hingga Correlation Immunity (CI)[cite: 31, 37].</div>
<div class="metric-tag-container" style="margin-top:10px;">
<span class="workflow-tag">NL &ge; 112</span>
<span class="workflow-tag">SAC &approx; 0.5</span>
<span class="workflow-tag">DU &le; 4</span>
</div>
</div>
</div>

<div class="workflow-item" style="border-left: none;">
<div class="workflow-step-num">STEP 06 // FINAL OPTIMIZATION</div>
<div class="workflow-card" style="border-color: #00f2fe;">
<div class="workflow-title" style="color: #00f2fe;">Pemilihan Matriks K44</div>
<div class="workflow-desc">Berdasarkan komparasi metrik, konfigurasi K44 terpilih sebagai yang paling optimal dibandingkan standar AES.</div>
<div class="workflow-tag" style="background: rgba(0, 242, 254, 0.2);">Best Performer: K44</div>
</div>
</div>

</div>
"""

st.markdown(workflow_content, unsafe_allow_html=True)

# === SECTION: WORKFLOW SUMMARY ===

workflow_details = """
<div class="workflow-container" style="margin-top: -20px; padding-top: 0;">

<div class="wf-summary-grid">
<div class="wf-summary-card">
<div class="step-label">MATRIKS AFFINE</div>
<div style="font-size: 1.8rem; font-weight: 700; color: #fff; font-family: 'Rajdhani';">2⁶⁴</div>
<p style="font-size: 0.75rem; color: #888; margin-top: 5px;">Kombinasi 8x8 bit potensial (18.4x10¹⁸).</p>
</div>
<div class="wf-summary-card">
<div class="step-label">KANDIDAT S-BOX</div>
<div style="font-size: 1.8rem; font-weight: 700; color: #fff; font-family: 'Rajdhani';">2⁶⁴</div>
<p style="font-size: 0.75rem; color: #888; margin-top: 5px;">Membentuk satu S-box unik tiap matriks.</p>
</div>
<div class="wf-summary-card">
<div class="step-label">S-BOX VALID</div>
<div style="font-size: 1.8rem; font-weight: 700; color: #fff; font-family: 'Rajdhani';">128</div>
<p style="font-size: 0.75rem; color: #888; margin-top: 5px;">Lolos kriteria Bijective & Balance.</p>
</div>
<div class="wf-summary-card" style="border-color: rgba(0, 242, 254, 0.3);">
<div class="step-label">TERBAIK (PAPER)</div>
<div style="font-size: 1.8rem; font-weight: 700; color: #00f2fe; font-family: 'Rajdhani';">K44</div>
<p style="font-size: 0.75rem; color: #888; margin-top: 5px;">Unggul setelah 10 pengujian kriptografi.</p>
</div>
</div>

<div class="wf-detail-grid">
<div class="wf-detail-card">
<div style="color: #fff; font-weight: 700; margin-bottom: 8px; font-family: 'Rajdhani'; text-transform: uppercase;">Balance</div>
<p style="font-size: 0.85rem; color: #8899ac; line-height: 1.5;">Distribusi bit keluaran harus memiliki jumlah 0 dan 1 yang identik (128 masing-masing) untuk mencegah bias statistik.</p>
</div>
<div class="wf-detail-card">
<div style="color: #fff; font-weight: 700; margin-bottom: 8px; font-family: 'Rajdhani'; text-transform: uppercase;">Bijective</div>
<p style="font-size: 0.85rem; color: #8899ac; line-height: 1.5;">Seluruh nilai (0–255) muncul tepat satu kali tanpa duplikasi, memastikan S-box dapat dibalik (invertible) sempurna.</p>
</div>
</div>

<div style="margin-top: 40px; background: rgba(255,255,255,0.02); padding: 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
<div style="color: #fff; font-family: 'Rajdhani'; font-size: 1.2rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">10 Pengujian Kriptografi Utama</div>
<p style="color: #8899ac; font-size: 0.85rem; margin-top: 5px;">Metrik keamanan yang digunakan untuk memverifikasi ketahanan S-box terhadap serangan linier dan diferensial.</p>

<div class="metric-pill-container">
<span class="metric-pill">Nonlinearity (NL)</span>
<span class="metric-pill">Strict Avalanche Criterion (SAC)</span>
<span class="metric-pill">Bit Independence Criterion - NL</span>
<span class="metric-pill">Bit Independence Criterion - SAC</span>
<span class="metric-pill">Linear Approx. Probability (LAP)</span>
<span class="metric-pill">Differential Approx. Prob. (DAP)</span>
<span class="metric-pill">Differential Uniformity (DU)</span>
<span class="metric-pill">Algebraic Degree (AD)</span>
<span class="metric-pill">Transparency Order (TO)</span>
<span class="metric-pill">Correlation Immunity (CI)</span>
</div>
</div>

<p style="color: #52525b; font-size: 0.75rem; margin-top: 25px; font-style: italic;">
* Seluruh tahapan validasi dan pengujian di atas diimplementasikan secara otomatis dalam sistem backend untuk memastikan integritas data S-box yang dihasilkan.
</p>

</div>
"""

st.markdown(workflow_details, unsafe_allow_html=True)

# === SECTION: METRIC COMPARISON TABLE ===
st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <h2 class="tech-font">METRIC COMPARISON ANALYSIS</h2>
    <p style="color: #888;">Benchmarking Research K44 against AES Rijndael Standard </p>
</div>
""", unsafe_allow_html=True)

comparison_html = """
<table class="comparison-table">
<thead>
<tr>
<th>Parameter Metrik</th>
<th>AES Standard (Reference)</th>
<th>K44 (Research Result)</th>
<th>Interpretasi Ideal</th>
</tr>
</thead>
<tbody>
<tr>
<td class="metric-name">Nonlinearity (NL)</td>
<td>112</td>
<td class="highlight-k44">112</td>
<td>Maksimal (Semakin Tinggi Semakin Baik)</td>
</tr>
<tr>
<td class="metric-name">Differential Uniformity (DU)</td>
<td>4</td>
<td class="highlight-k44">4</td>
<td>Minimal (Resisten thd Differential Attack)</td>
</tr>
<tr>
<td class="metric-name">Strict Avalanche Criterion (SAC)</td>
<td>0.5005</td>
<td class="highlight-k44">0.5007</td>
<td>Mendekati 0.5 (Ideal Bit Diffusion)</td>
</tr>
<tr>
<td class="metric-name">Bit Independence Criterion (BIC-NL)</td>
<td>112</td>
<td class="highlight-k44">112</td>
<td>Maksimal (Independensi Bit Output)</td>
</tr>
<tr>
<td class="metric-name">Linear Approx. Probability (LAP)</td>
<td>0.0625</td>
<td class="highlight-k44">0.0625</td>
<td>Minimal (Resisten thd Linear Attack)</td>
</tr>
<tr>
<td class="metric-name">Differential Approx. Prob. (DAP)</td>
<td>0.0156</td>
<td class="highlight-k44">0.0156</td>
<td>Minimal (Kekuatan Struktur S-Box)</td>
</tr>
<tr>
<td class="metric-name">Algebraic Degree (AD)</td>
<td>7</td>
<td class="highlight-k44">7</td>
<td>Maksimal (Kompleksitas Aljabar)</td>
</tr>
<tr>
<td class="metric-name">Transparency Order (TO)</td>
<td>7.860</td>
<td class="highlight-k44">7.858</td>
<td>Minimal (Resisten thd Side-Channel Attack)</td>
</tr>
<tr>
<td class="metric-name">Correlation Immunity (CI)</td>
<td>0</td>
<td class="highlight-k44">0</td>
<td>Minimal (Independensi Input-Output)</td>
</tr>
</tbody>
</table>
<p style="color: #52525b; font-size: 0.8rem; margin-top: 15px; font-style: italic;">
* Berdasarkan paper riset, konfigurasi matriks K44 menghasilkan properti kriptografi yang identik atau bahkan sedikit lebih unggul dalam aspek ketahanan serangan fisik dibandingkan standar AES.
</p>
"""

st.markdown(comparison_html, unsafe_allow_html=True)

# ==========================================
# 6. IMPLEMENTASI ENKRIPSI & DEKRIPSI (AES-CBC) + ANALISIS (UPDATED DESIGN)
# ==========================================

# --- A. DEFINISI S-BOX & HELPER CLASSES ---
# (Data S-BOX dan Class MiniAES tetap sama seperti sebelumnya, hanya disembunyikan untuk kerapihan)
K44_SBOX_TABLE = [
    99, 205, 85, 71, 25, 127, 113, 219, 63, 244, 109, 159, 11, 228, 94, 214,
    77, 177, 201, 78, 5, 48, 29, 30, 87, 96, 193, 80, 156, 200, 216, 86,
    116, 143, 10, 14, 54, 169, 148, 68, 49, 75, 171, 157, 92, 114, 188, 194,
    121, 220, 131, 210, 83, 135, 250, 149, 253, 72, 182, 33, 190, 141, 249, 82,
    232, 50, 21, 84, 215, 242, 180, 198, 168, 167, 103, 122, 152, 162, 145, 184,
    43, 237, 119, 183, 7, 12, 125, 55, 252, 206, 235, 160, 140, 133, 179, 192,
    110, 176, 221, 134, 19, 6, 187, 59, 26, 129, 112, 73, 175, 45, 24, 218,
    44, 66, 151, 32, 137, 31, 35, 147, 236, 247, 117, 132, 79, 136, 154, 105,
    199, 101, 203, 52, 57, 4, 153, 197, 88, 76, 202, 174, 233, 62, 208, 91,
    231, 53, 1, 124, 0, 28, 142, 170, 158, 51, 226, 65, 123, 186, 239, 246,
    38, 56, 36, 108, 8, 126, 9, 189, 81, 234, 212, 224, 13, 3, 40, 64,
    172, 74, 181, 118, 39, 227, 130, 89, 245, 166, 16, 61, 106, 196, 211, 107,
    229, 195, 138, 18, 93, 207, 240, 95, 58, 255, 209, 217, 15, 111, 46, 173,
    223, 42, 115, 238, 139, 243, 23, 98, 100, 178, 37, 97, 191, 213, 222, 155,
    165, 2, 146, 204, 120, 241, 163, 128, 22, 90, 60, 185, 67, 34, 27, 248,
    164, 69, 41, 230, 104, 47, 144, 251, 20, 17, 150, 225, 254, 161, 102, 70
]

AES_SBOX_DECIMAL = [
    99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
    202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
    183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
    4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
    9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
    83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
    208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
    81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
    205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
    96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219,
    224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121,
    231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8,
    186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138,
    112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
    225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223,
    140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22
]


class MiniAES:
    def __init__(self, key, sbox):
        self.sbox = sbox
        self.inv_sbox = [0] * 256
        for i, v in enumerate(sbox):
            self.inv_sbox[v] = i
        self.round_keys = self._key_expansion(key)

    def _sub_bytes(self, state, inv=False):
        box = self.inv_sbox if inv else self.sbox
        for r in range(4):
            for c in range(4):
                state[r][c] = box[state[r][c]]
        return state

    def _shift_rows(self, state, inv=False):
        if inv:
            state[1][1], state[1][2], state[1][3], state[1][0] = state[1][0], state[1][1], state[1][2], state[1][3]
            state[2][2], state[2][3], state[2][0], state[2][1] = state[2][0], state[2][1], state[2][2], state[2][3]
            state[3][3], state[3][0], state[3][1], state[3][2] = state[3][0], state[3][1], state[3][2], state[3][3]
        else:
            state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
            state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
            state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]
        return state

    def _gmix_column(self, r):
        a = [0] * 4
        b = [0] * 4
        for c in range(4):
            a[c] = r[c]
            h = r[c] & 0x80
            b[c] = (r[c] << 1) & 0xFF
            if h == 0x80:
                b[c] ^= 0x1b
        r[0] = b[0] ^ a[3] ^ a[2] ^ b[1] ^ a[1]
        r[1] = b[1] ^ a[0] ^ a[3] ^ b[2] ^ a[2]
        r[2] = b[2] ^ a[1] ^ a[0] ^ b[3] ^ a[3]
        r[3] = b[3] ^ a[2] ^ a[1] ^ b[0] ^ a[0]
        return r

    def _mix_columns(self, state, inv=False):
        for i in range(4):
            if inv:
                col = [state[0][i], state[1][i], state[2][i], state[3][i]]
                col = self._inv_mix_column(col)
                for j in range(4):
                    state[j][i] = col[j]
            else:
                col = [state[0][i], state[1][i], state[2][i], state[3][i]]
                col = self._gmix_column(col)
                for j in range(4):
                    state[j][i] = col[j]
        return state

    def _inv_mix_column(self, col):
        u = self._xtime(self._xtime(col[0] ^ col[2]))
        v = self._xtime(self._xtime(col[1] ^ col[3]))
        col[0] ^= u
        col[1] ^= v
        col[2] ^= u
        col[3] ^= v
        return self._gmix_column(col)

    def _xtime(self, a):
        return (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

    def _add_round_key(self, state, k):
        for r in range(4):
            for c in range(4):
                state[r][c] ^= k[r][c]
        return state

    def _key_expansion(self, key):
        w = [key[i:i+4] for i in range(0, len(key), 4)]
        rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
        while len(w) < 44:
            temp = w[-1]
            if len(w) % 4 == 0:
                temp = temp[1:] + temp[:1]
                temp = [self.sbox[b] for b in temp]
                temp[0] ^= rcon[len(w)//4 - 1]
            w.append([a ^ b for a, b in zip(w[-4], temp)])
        round_keys = []
        for i in range(0, len(w), 4):
            round_keys.append(list(zip(*w[i:i+4])))
        return round_keys

    def encrypt_block(self, plaintext):
        state = [list(x) for x in zip(*[plaintext[i:i+4]
                                        for i in range(0, 16, 4)])]
        state = self._add_round_key(state, self.round_keys[0])
        for i in range(1, 10):
            state = self._sub_bytes(state)
            state = self._shift_rows(state)
            state = self._mix_columns(state)
            state = self._add_round_key(state, self.round_keys[i])
        state = self._sub_bytes(state)
        state = self._shift_rows(state)
        state = self._add_round_key(state, self.round_keys[10])
        return [state[r][c] for c in range(4) for r in range(4)]

    def decrypt_block(self, ciphertext):
        state = [list(x) for x in zip(*[ciphertext[i:i+4]
                                        for i in range(0, 16, 4)])]
        state = self._add_round_key(state, self.round_keys[10])
        for i in range(9, 0, -1):
            state = self._shift_rows(state, inv=True)
            state = self._sub_bytes(state, inv=True)
            state = self._add_round_key(state, self.round_keys[i])
            state = self._mix_columns(state, inv=True)
        state = self._shift_rows(state, inv=True)
        state = self._sub_bytes(state, inv=True)
        state = self._add_round_key(state, self.round_keys[0])
        return [state[r][c] for c in range(4) for r in range(4)]


def pad_pkcs7(data):
    block_size = 16
    padding_len = block_size - (len(data) % block_size)
    return data + bytes([padding_len] * padding_len)


def unpad_pkcs7(data):
    if not data:
        return data
    padding_len = data[-1]
    if padding_len < 1 or padding_len > 16:
        return data
    return data[:-padding_len]


def process_aes(sbox_type, operation, key_text, input_bytes):
    raw_key = key_text.encode('utf-8')
    if len(raw_key) > 16:
        key = raw_key[:16]
    else:
        key = raw_key + b'\0' * (16 - len(raw_key))

    if sbox_type == "AES Standard":
        selected_sbox = AES_SBOX_DECIMAL
    else:
        selected_sbox = K44_SBOX_TABLE

    aes = MiniAES(list(key), selected_sbox)
    result = bytearray()
    iv = [0] * 16

    if operation == "Enkripsi":
        padded_input = pad_pkcs7(input_bytes)
        prev_block = iv
        for i in range(0, len(padded_input), 16):
            block = list(padded_input[i:i+16])
            block_xored = [b ^ p for b, p in zip(block, prev_block)]
            enc_block = aes.encrypt_block(block_xored)
            result.extend(enc_block)
            prev_block = enc_block
    else:
        prev_block = iv
        for i in range(0, len(input_bytes), 16):
            block = list(input_bytes[i:i+16])
            if len(block) == 16:
                dec_block = aes.decrypt_block(block)
                plain_block = [d ^ p for d, p in zip(dec_block, prev_block)]
                result.extend(plain_block)
                prev_block = block
        try:
            result = unpad_pkcs7(result)
        except:
            pass
    return bytes(result)


def calculate_entropy(data_bytes):
    import math
    if not data_bytes:
        return 0
    counts = [0] * 256
    for b in data_bytes:
        counts[b] += 1
    total = len(data_bytes)
    entropy = 0
    for c in counts:
        if c > 0:
            p = c / total
            entropy -= p * math.log2(p)
    return entropy


def calculate_correlation(image_data, width, height):
    import numpy as np
    if len(image_data) != width * height * 3:
        return 0, 0, 0
    arr = np.array(list(image_data)).reshape(height, width, 3)
    channel = arr[:, :, 0].astype(float)

    def get_corr(x, y):
        if len(x) == 0:
            return 0
        if np.std(x) == 0 or np.std(y) == 0:
            return 0
        return np.abs(np.corrcoef(x, y)[0, 1])
    h_x, h_y = channel[:, :-1].flatten(), channel[:, 1:].flatten()
    v_x, v_y = channel[:-1, :].flatten(), channel[1:, :].flatten()
    d_x, d_y = channel[:-1, :-1].flatten(), channel[1:, 1:].flatten()
    return get_corr(h_x, h_y), get_corr(v_x, v_y), get_corr(d_x, d_y)


def calculate_npcr_uaci(cipher1_bytes, cipher2_bytes):
    import numpy as np
    min_len = min(len(cipher1_bytes), len(cipher2_bytes))
    c1 = np.array(list(cipher1_bytes[:min_len]), dtype=int)
    c2 = np.array(list(cipher2_bytes[:min_len]), dtype=int)
    diff = (c1 != c2).astype(int)
    npcr = (np.sum(diff) / min_len) * 100
    abs_diff = np.abs(c1 - c2)
    uaci = (np.sum(abs_diff) / (255 * min_len)) * 100
    return npcr, uaci


def get_status_entropy(val):
    if val >= 7.99:
        return "Excellent", "#28a745"
    if val >= 7.95:
        return "Good", "#17a2b8"
    if val >= 7.5:
        return "Fair", "#ffc107"
    return "Poor", "#dc3545"


def get_status_npcr(val):
    if val >= 99.60:
        return "Excellent", "#28a745"
    if val >= 99.50:
        return "Good", "#17a2b8"
    if val >= 99.0:
        return "Fair", "#ffc107"
    return "Poor", "#dc3545"


def get_status_uaci(val):
    diff = abs(val - 33.46)
    if diff <= 0.5:
        return "Excellent", "#28a745"
    if diff <= 1.0:
        return "Good", "#17a2b8"
    if diff <= 2.0:
        return "Fair", "#ffc107"
    return "Poor", "#dc3545"


def get_status_corr(val):
    if val <= 0.01:
        return "Excellent", "#28a745"
    if val <= 0.05:
        return "Good", "#17a2b8"
    if val <= 0.1:
        return "Fair", "#ffc107"
    return "Poor", "#dc3545"


def render_metric_card(title, value_str, sub_value, status, color, ideal_str):
    st.markdown(f"""
    <div style="background-color: #262626; padding: 15px; border-radius: 10px; border: 1px solid #444; margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
            <span style="color: #aaa; font-size: 0.9em; font-weight: bold;">{title}</span>
            <span style="background-color: {color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75em;">{status}</span>
        </div>
        <div style="font-size: 1.8em; font-weight: bold; color: white;">{value_str}</div>
        <div style="color: #888; font-size: 0.85em; margin-top: 5px;">
            Original: {sub_value}<br>
            <span style="color: #aaa; font-style: italic;">Target: {ideal_str}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- B. UI IMPLEMENTATION (Updated Design) ---

st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; margin-bottom: 40px; animation: fadeInUp 0.8s ease;'><h2>🔐 ENCRYPTION & DESCRIPTION IMPLEMENTATION</h2></div>", unsafe_allow_html=True)

# Wrap everything in the card container
with st.container():

    st.markdown("""
        <div class="panel-header">
            <div class="panel-title">AES-128 CBC Mode Engine</div>
            <div class="panel-subtitle">Secure data transmission simulation with PKCS#7 Padding</div>
        </div>
    """, unsafe_allow_html=True)

    impl_tab1, impl_tab2 = st.tabs(
        ["📝 TEXT ENCRYPTION", "🖼️ IMAGE ENCRYPTION"])

    # === TAB 1: TEXT ===
    with impl_tab1:
        col_t1, col_t2 = st.columns(2)
    with col_t1:
        op_text = st.radio("Operasi", ["Enkripsi", "Dekripsi"], key="op_text", horizontal=True)
        sbox_text = st.selectbox("Pilih S-Box", ["K44 (Research Paper)", "AES Standard"], key="sb_text")
    with col_t2:
        key_input_text = st.text_input("Kunci (Key) - Max 16 Byte", value="ResearchKey12345", key="k_text")
    
default_text = "Kami adalah orang-orang tampan dan pemberani penakluk para wanita"
txt_input = st.text_area("Input Teks", value=default_text, height=100)
    
if st.button("Proses Teks", use_container_width=True):
    if not txt_input:
        st.warning("Mohon isi input teks.")
    else:
        try:
            import base64
            if op_text == "Enkripsi":
                data_in = txt_input.encode('utf-8')
                # Encrypt (Random IV generated inside)
                res = process_aes(sbox_text, "Enkripsi", key_input_text, data_in)
                out_b64 = base64.b64encode(res).decode('utf-8')
                st.success("Enkripsi Berhasil!")
                st.code(out_b64, language="text")
            else:
                try:
                    data_in = base64.b64decode(txt_input)
                    res = process_aes(sbox_text, "Dekripsi", key_input_text, data_in)
                    st.success("Dekripsi Berhasil!")
                    st.code(res.decode('utf-8', errors='ignore'), language="text")
                except Exception as e:
                    st.error(f"Gagal dekripsi: {e}")
        except Exception as e:
            st.error(f"Error: {e}")

# === TAB 2: IMAGE + ANALYSIS ===
with impl_tab2:
    st.info("Mode CBC digunakan dengan Random IV. Gambar akan di-resize maks 200px.")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        op_img = st.radio("Operasi", ["Enkripsi", "Dekripsi"], key="op_img", horizontal=True)
        sbox_img = st.selectbox("Pilih S-Box", ["K44 (Research Paper)", "AES Standard"], key="sb_img")
    
    with col_i2:
        key_input_img = st.text_input("Kunci (Key)", value="ResearchKey12345", key="k_img")

    upl_file = st.file_uploader("Upload Gambar", type=["png", "jpg", "jpeg", "bmp"])
    
    if st.button("Proses Gambar & Analisis", use_container_width=True):
        if upl_file:
            try:
                image = Image.open(upl_file).convert('RGB')
                w, h = image.size
                if w > 200:
                    ratio = 200 / w
                    image = image.resize((200, int(h * ratio)))
                    w, h = image.size
                
                pixels = list(image.getdata())
                flat_pixels = [item for sublist in pixels for item in sublist]
                raw_data = bytes(flat_pixels)
                
                with st.spinner("Memproses..."):
                    # Proses Utama (Random IV)
                    processed_data = process_aes(sbox_img, op_img, key_input_img, raw_data)
                
                if op_img == "Enkripsi":
                    # --- PREPARE VISUALIZATION ---
                    # Cut IV (16 bytes) for visualization purpose to keep image dimensions
                    # Data Structure: [IV 16 bytes] [Encrypted Pixels .....]
                    # We only visualize the Encrypted Pixels part
                    
                    encrypted_pixel_data = processed_data[16:] 
                    req_len = len(flat_pixels)
                    vis_data = encrypted_pixel_data[:req_len]
                    if len(vis_data) < req_len: vis_data += b'\x00' * (req_len - len(vis_data))
                    
                    enc_image = Image.frombytes('RGB', image.size, vis_data)
                    
                    c_img1, c_img2 = st.columns(2)
                    c_img1.image(image, caption="Original Image", use_container_width=True)
                    c_img2.image(enc_image, caption=f"Encrypted (CBC Mode)", use_container_width=True)
                    
                    # --- 1. HISTOGRAM ANALYSIS ---
                    st.markdown("### 📊 Histogram Analysis")
                    hist_orig = image.histogram()
                    hist_enc = enc_image.histogram()
                    
                    def plot_rgb_hist(hist_data, title):
                        fig, ax = plt.subplots(figsize=(6, 2.5))
                        ax.set_title(title, color='white', fontsize=10)
                        ax.set_xlim(0, 255)
                        ax.grid(color='#333', linestyle='--', linewidth=0.5)
                        ax.axis('off')
                        
                        r = hist_data[0:256]
                        g = hist_data[256:512]
                        b = hist_data[512:768]
                        x = np.arange(256)
                        ax.fill_between(x, r, color='red', alpha=0.3)
                        ax.fill_between(x, g, color='green', alpha=0.3)
                        ax.fill_between(x, b, color='blue', alpha=0.3)
                        fig.patch.set_alpha(0)
                        ax.patch.set_alpha(0)
                        return fig

                    c_h1, c_h2 = st.columns(2)
                    c_h1.pyplot(plot_rgb_hist(hist_orig, "Original Histogram"))
                    c_h2.pyplot(plot_rgb_hist(hist_enc, "Encrypted Histogram (Flat = Secure)"))
                    
                    # --- 2. SECURITY METRICS CARDS ---
                    st.markdown("### 🛡 Security Metrics Analysis")
                    
                    with st.spinner("Calculating Security Metrics..."):
                        # Entropy & Correlation (Use Visual Data)
                        entropy_orig = calculate_entropy(raw_data)
                        entropy_enc = calculate_entropy(vis_data)
                        
                        corr_orig = calculate_correlation(raw_data, w, h)
                        corr_enc = calculate_correlation(vis_data, w, h)
                        avg_corr_enc = sum(corr_enc)/3 
                        
                        # Differential (NPCR/UACI)
                        # SPECIAL HANDLING:
                        # To test algorithm sensitivity, we must use the SAME IV for both images.
                        # Otherwise, we are just measuring Random IV effect.
                        
                        # 1. Extract IV used in the main encryption
                        used_iv = processed_data[:16]
                        
                        # 2. Prepare Modified Plaintext (Flip 1 bit in 1st byte)
                        raw_data_mod = bytearray(raw_data)
                        raw_data_mod[0] ^= 1 
                        
                        # 3. Encrypt Modified Plaintext with SAME IV
                        cipher2 = process_aes(sbox_img, "Enkripsi", key_input_img, bytes(raw_data_mod), forced_iv=used_iv)
                        
                        # 4. Compare (Skip IVs for comparison)
                        npcr, uaci = calculate_npcr_uaci(processed_data[16:], cipher2[16:])

                    row1_1, row1_2 = st.columns(2)
                    with row1_1:
                        stat, col = get_status_entropy(entropy_enc)
                        render_metric_card("Entropy", f"{entropy_enc:.4f}", f"{entropy_orig:.4f}", stat, col, "Ideal: 8.0")
                    with row1_2:
                        stat, col = get_status_npcr(npcr)
                        render_metric_card("NPCR (Differential)", f"{npcr:.4f}%", "N/A", stat, col, "Ideal: > 99.6%")

                    row2_1, row2_2 = st.columns(2)
                    with row2_1:
                        stat, col = get_status_uaci(uaci)
                        render_metric_card("UACI (Differential)", f"{uaci:.4f}%", "N/A", stat, col, "Ideal: ~33.46%")
                    with row2_2:
                        stat, col = get_status_corr(avg_corr_enc)
                        render_metric_card("Correlation (Avg)", f"{avg_corr_enc:.4f}", f"{sum(corr_orig)/3:.4f}", stat, col, "Ideal: 0.0")

                    st.download_button("Download Encrypted Bytes", processed_data, "encrypted.bin")
                    
                else:
                    # DEKRIPSI CBC
                    # Extract IV -> Decrypt -> Unpad
                    req_len = len(raw_data)
                    vis_data = processed_data[:req_len]
                    try:
                        dec_image = Image.frombytes('RGB', image.size, vis_data)
                        st.image(dec_image, caption="Hasil Dekripsi")
                        st.success("Dekripsi selesai.")
                    except:
                        st.warning("Visualisasi dekripsi mungkin tidak sempurna.")
            except Exception as e:
                st.error(f"Error processing: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
    
# === SECTION: FOOTER ===
footer_content = """
<div class="footer-container">
<div class="footer-content-wrapper">
<div class="footer-grid">
<div>
<div class="footer-brand-title">S-BOX LAB <span style="color:#00f2fe;">💠</span></div>
<p style="color:#8899ac; font-size:0.85rem; line-height:1.6;">
Platform analisis kriptografi tingkat lanjut yang berfokus pada eksplorasi matriks affine dan optimasi properti S-box AES-128.
</p>
</div>
<div>
<div class="footer-heading">Navigasi</div>
<a href="#" class="footer-link">Research Workflow</a>
<a href="#" class="footer-link">Metric Analysis</a>
<a href="#" class="footer-link">Experimental Lab</a>
</div>
<div>
<div class="footer-heading">Tim Riset</div>
<div class="footer-link">Wisely</div>
<div class="footer-link">Roihan</div>
<div class="footer-link">Khayri</div>
<div class="footer-link">Byan</div>
</div>
<div>
<div class="footer-heading">Afiliasi</div>
<p style="color:#8899ac; font-size:0.85rem; line-height:1.6;">
Teknik Informatika<br>
Universitas Negeri Semarang<br>
Semarang, Indonesia
</p>
</div>
</div>
<div class="footer-bottom">
&copy; 2025 S-Box Research Lab | UNNES Informatics Engineering.
</div>
</div>
</div>
"""

st.markdown(footer_content, unsafe_allow_html=True)