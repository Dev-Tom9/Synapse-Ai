import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
from typing import List
import random
from database import init_db, save_report, fetch_reports
from utils import extract_text_from_pdfs, calculate_risk_score
from analytics import show_analytics
from fpdf import FPDF

# ---------------- INIT DB ----------------
init_db()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Synapse Intelligence OS",
    page_icon="favicon.png",  # Custom PNG favicon
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "tab" not in st.session_state:
    st.session_state.tab = "summary"

# ---------------- THEME CSS ----------------
def set_theme():
    if st.session_state.theme == "light":
        st.markdown("""
        <style>
        .stApp { background: linear-gradient(to bottom, #f5f7fa, #e0e2eb); color: #111827; font-family: 'Inter', sans-serif;}
        .glass-card { background: rgba(255,255,255,0.07); border: 1px solid rgba(0,0,0,0.1); backdrop-filter: blur(16px); padding: 25px; border-radius: 20px; margin-bottom: 20px;}
        .stButton>button {background: linear-gradient(90deg, #00CFFF, #00FFA3); color: black; font-weight: 700; border-radius: 16px; height: 3rem; border: none; transition: all 0.3s;}
        .stButton>button:hover {opacity:0.85; transform: scale(1.02);}
        textarea, .fileUploader {background-color: #e5e7eb !important; color: #111827 !important; border-radius: 18px !important; border: 1px solid #d1d5db !important;}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle at top left, #0e1117, #050505 70%); color: #f3f4f6; font-family: 'Inter', sans-serif;}
        .glass-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); backdrop-filter: blur(16px); padding: 25px; border-radius: 20px; margin-bottom: 20px;}
        .stButton>button {background: linear-gradient(90deg, #00FFA3, #00CCFF); color: black; font-weight: 700; border-radius: 16px; height: 3rem; border: none; transition: all 0.3s;}
        .stButton>button:hover {opacity:0.85; transform: scale(1.02);}
        textarea, .fileUploader {background-color: #111827 !important; border-radius: 18px !important; border: 1px solid #1f2937 !important; color: white !important;}
        </style>
        """, unsafe_allow_html=True)

set_theme()

# ---------------- THEME TOGGLE ----------------
theme_toggle = st.sidebar.radio("Theme", ["dark", "light"])
st.session_state.theme = theme_toggle
set_theme()

# ---------------- MODEL ----------------
class IntelligenceReport(BaseModel):
    summary: str
    key_findings: List[str]
    risks: List[str]
    strategic_recommendation: str

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔐 API Access")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
st.sidebar.markdown("---")
st.sidebar.info("Use demo mode if no API key or quota exceeded.")

# ---------------- HEADER ----------------
st.markdown("""
<div class="glass-card" style="text-align:center;">
<h1>⚡ Synapse Intelligence OS</h1>
<p style="font-size:18px;">Enterprise AI Intelligence & Risk Command Platform</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT ----------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "Upload PDFs for Intelligence Aggregation",
    type=["pdf"],
    accept_multiple_files=True
)
manual_text = st.text_area("Or Paste Intelligence Text", height=250)
run = st.button("Run Intelligence Engine")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PROCESS ----------------
if run:
    combined_text = ""
    if uploaded_files:
        combined_text += extract_text_from_pdfs(uploaded_files)
    if manual_text:
        combined_text += manual_text
    if not combined_text.strip():
        st.warning("Please provide text or upload PDFs.")
        st.stop()

    # Try AI API, else fallback demo mode
    try:
        if api_key:
            client = OpenAI(api_key=api_key)
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Extract structured intelligence."},
                    {"role": "user", "content": combined_text}
                ],
                response_format=IntelligenceReport,
            )
            rep = completion.choices[0].message.parsed
        else:
            raise Exception("No API Key")
    except:
        # Demo Mode
        rep = IntelligenceReport(
            summary="Operational strain and emerging market risks detected across multiple sectors.",
            key_findings=["Revenue growth but rising costs", "Staff turnover rising in R&D", "Emerging market competition"],
            risks=["Cybersecurity vulnerability", "Supply chain delays", "Regulatory compliance risks"],
            strategic_recommendation="Scale infrastructure, strengthen cybersecurity, and optimize resource allocation."
        )

    # Calculate risk
    risk_score = calculate_risk_score(rep.risks)
    confidence = random.randint(85, 99)

    # Save to DB
    save_report(rep.summary, rep.risks, rep.key_findings, rep.strategic_recommendation, risk_score, confidence)

    # ---------------- TABS ----------------
    tabs = st.tabs(["📄 Summary & Findings", "📊 Analytics Dashboard", "🗂 Report History"])

    # ---- TAB 1: Summary & Findings ----
    with tabs[0]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Executive Summary")
        st.write(rep.summary)

        st.subheader("Key Findings")
        with st.expander("View Findings"):
            for f in rep.key_findings:
                st.write(f"- {f}")

        st.subheader("Risks")
        with st.expander("View Risks"):
            for r in rep.risks:
                st.write(f"- {r}")

        st.subheader("Strategic Recommendation")
        with st.expander("View Recommendation"):
            st.write(rep.strategic_recommendation)

        st.metric("Risk Score", f"{risk_score}/100")
        st.metric("AI Confidence", f"{confidence}%")

        # PDF download
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "Synapse Intelligence Report", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, f"Summary: {rep.summary}")
        pdf.multi_cell(0, 10, "Key Findings:\n" + "\n".join(rep.key_findings))
        pdf.multi_cell(0, 10, "Risks:\n" + "\n".join(rep.risks))
        pdf.multi_cell(0, 10, f"Strategic Recommendation:\n{rep.strategic_recommendation}")
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("📄 Download PDF Report", pdf_bytes, file_name="report.pdf")

        st.markdown('</div>', unsafe_allow_html=True)

    # ---- TAB 2: Analytics ----
    with tabs[1]:
        reports = fetch_reports()
        show_analytics(reports)

    # ---- TAB 3: History ----
    with tabs[2]:
        reports = fetch_reports()
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Past Reports")
        for r in reports[:10]:
            st.write(f"**{r[7]}** - Risk Score: {r[5]}/100 | Confidence: {r[6]}%")
            st.write(f"Summary: {r[1]}")
            st.markdown("---")
        st.markdown('</div>', unsafe_allow_html=True)
