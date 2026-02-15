import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from fpdf import FPDF
from datetime import datetime

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Synapse Intelligence OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# GLOBAL STYLING
# ===============================
st.markdown("""
<style>

/* Remove default padding */
.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* App background */
.stApp {
    background: radial-gradient(circle at top left, #0e1117, #050505 70%);
    color: #f3f4f6;
    font-family: 'Inter', sans-serif;
}

/* Hero section */
.hero {
    padding: 40px 0px 20px 0px;
}

.hero h1 {
    font-size: 52px;
    font-weight: 800;
    margin-bottom: 0px;
}

.hero p {
    font-size: 18px;
    color: #9ca3af;
}

/* Status badge */
.status-badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 50px;
    background: rgba(0,255,163,0.1);
    color: #00FFA3;
    font-size: 14px;
    margin-top: 10px;
}

/* Cards */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 20px;
    transition: 0.3s ease;
}

.glass-card:hover {
    border: 1px solid rgba(0,255,163,0.4);
    transform: translateY(-3px);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #00FFA3, #00CCFF);
    color: black;
    font-weight: 700;
    border-radius: 14px;
    height: 3rem;
    border: none;
}

.stButton>button:hover {
    box-shadow: 0px 0px 25px rgba(0,255,163,0.5);
}

/* Text area */
textarea {
    background-color: #111827 !important;
    border-radius: 16px !important;
    border: 1px solid #1f2937 !important;
    color: white !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)


# ===============================
# DATA MODEL
# ===============================
class IntelligenceReport(BaseModel):
    summary: str
    key_findings: List[str]
    risks: List[str]
    strategic_recommendation: str


# ===============================
# PDF GENERATOR
# ===============================
def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="SYNAPSE INTELLIGENCE REPORT", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, txt=f"Summary:\n{data.summary}")
    pdf.ln(5)

    pdf.multi_cell(0, 8, txt="Key Findings:")
    for f in data.key_findings:
        pdf.multi_cell(0, 8, txt=f"- {f}")

    pdf.ln(5)
    pdf.multi_cell(0, 8, txt="Risks:")
    for r in data.risks:
        pdf.multi_cell(0, 8, txt=f"- {r}")

    pdf.ln(5)
    pdf.multi_cell(0, 8, txt=f"Strategic Recommendation:\n{data.strategic_recommendation}")

    return pdf.output(dest='S').encode('latin-1')


# ===============================
# HERO SECTION
# ===============================
st.markdown("""
<div class="hero">
    <h1>⚡ Synapse Intelligence OS</h1>
    <p>Strategic AI Intelligence Extraction & Risk Profiling Engine</p>
    <div class="status-badge">● SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ===============================
# DASHBOARD METRICS
# ===============================
colA, colB, colC = st.columns(3)

with colA:
    st.markdown('<div class="glass-card"><h3>Reports Generated</h3><h2>128</h2></div>', unsafe_allow_html=True)

with colB:
    st.markdown('<div class="glass-card"><h3>Risk Signals</h3><h2>24 Active</h2></div>', unsafe_allow_html=True)

with colC:
    st.markdown('<div class="glass-card"><h3>System Confidence</h3><h2>97.4%</h2></div>', unsafe_allow_html=True)

st.divider()

# ===============================
# MAIN INTELLIGENCE CONSOLE
# ===============================
col1, col2 = st.columns([1,1])

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    source_text = st.text_area("Input Intelligence Corpus", height=350)
    run = st.button("Run Intelligence Engine")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if run and source_text:
        st.markdown('<div class="glass-card">Processing Intelligence...</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-card">Awaiting Intelligence Input...</div>', unsafe_allow_html=True)
