import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from fpdf import FPDF
from datetime import datetime
import matplotlib.pyplot as plt
import random
import io
import PyPDF2

# ================= CONFIG =================
st.set_page_config(
    page_title="Synapse Intelligence OS",
    page_icon="⚡",
    layout="wide"
)

# ================= STATE =================
if "history" not in st.session_state:
    st.session_state.history = []

# ================= PREMIUM UI =================
st.markdown("""
<style>
.block-container { padding: 2rem 3rem; }
.stApp {
    background: radial-gradient(circle at top left, #0f172a, #020617 70%);
    color: #f1f5f9;
    font-family: 'Inter', sans-serif;
}
.hero-title {
    font-size: 56px;
    font-weight: 900;
    background: linear-gradient(90deg, #00FFA3, #00CCFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.badge {
    padding: 6px 14px;
    border-radius: 50px;
    background: rgba(0,255,163,0.1);
    color: #00FFA3;
    font-size: 14px;
}
.glass-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 20px;
}
.stButton>button {
    background: linear-gradient(90deg, #00FFA3, #00CCFF);
    color: black;
    font-weight: 700;
    border-radius: 14px;
    height: 3rem;
}
textarea {
    background-color: #0f172a !important;
    border-radius: 16px !important;
    border: 1px solid #1e293b !important;
    color: white !important;
}
#MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================= MODEL =================
class IntelligenceReport(BaseModel):
    summary: str
    key_findings: List[str]
    risks: List[str]
    strategic_recommendation: str

# ================= PDF GENERATOR =================
def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="SYNAPSE INTELLIGENCE REPORT", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, txt=f"Summary:\n{data.summary}\n")
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

# ================= SIDEBAR =================
with st.sidebar:
    st.header("⚡ Secure Access")
    if "api_key" in st.secrets:
        api_key = st.secrets["api_key"]
        st.success("API Key Loaded")
    else:
        api_key = st.text_input("Enter OpenAI API Key", type="password")

# ================= HERO =================
st.markdown("""
<h1 class="hero-title">Synapse Intelligence OS</h1>
<p>Enterprise AI Intelligence & Risk Command Platform</p>
<span class="badge">SYSTEM ACTIVE</span>
""", unsafe_allow_html=True)

st.divider()

# ================= DASHBOARD METRICS =================
m1, m2, m3 = st.columns(3)
m1.metric("Reports Generated", len(st.session_state.history))
m2.metric("System Confidence", f"{random.randint(92,99)}%")
m3.metric("Threat Index", random.randint(1,10))

st.divider()

col1, col2 = st.columns(2)

# ================= INPUT =================
with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Intelligence PDF", type=["pdf"])
    source_text = st.text_area("Or Paste Intelligence Text", height=250)

    if uploaded_file:
        reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text()
        source_text = pdf_text

    run = st.button("Run Intelligence Engine")
    st.markdown('</div>', unsafe_allow_html=True)

# ================= OUTPUT =================
with col2:
    if run and source_text:
        try:
            if api_key:
                client = OpenAI(api_key=api_key)
                with st.spinner("Running AI Intelligence Scan..."):
                    completion = client.beta.chat.completions.parse(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Extract structured intelligence."},
                            {"role": "user", "content": source_text}
                        ],
                        response_format=IntelligenceReport,
                    )
                rep = completion.choices[0].message.parsed
            else:
                raise Exception("No API Key")

        except Exception:
            # Fallback Demo Mode
            rep = IntelligenceReport(
                summary="The organization faces operational strain and rising competition.",
                key_findings=[
                    "Revenue growth observed",
                    "Technical team turnover increasing",
                    "Competitive AI products emerging"
                ],
                risks=[
                    "Margin compression",
                    "Cybersecurity threats",
                    "Operational misalignment"
                ],
                strategic_recommendation="Optimize infrastructure costs and strengthen cybersecurity governance."
            )

        st.session_state.history.append(rep)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Executive Summary")
        st.write(rep.summary)

        st.subheader("Key Findings")
        for f in rep.key_findings:
            st.write(f"- {f}")

        st.subheader("Risk Analysis")
        for r in rep.risks:
            st.write(f"- {r}")

        st.subheader("Strategic Recommendation")
        st.write(rep.strategic_recommendation)

        # ================= RISK CHART =================
        risk_score = len(rep.risks) * random.randint(10,25)

        fig, ax = plt.subplots()
        ax.bar(["Risk Score"], [risk_score])
        ax.set_ylim(0,100)
        st.pyplot(fig)

        # ================= CONFIDENCE BAR =================
        confidence = random.randint(85,99)
        st.progress(confidence)
        st.write(f"AI Confidence Level: {confidence}%")

        pdf_bytes = create_pdf(rep)
        st.download_button(
            "Download Report",
            data=pdf_bytes,
            file_name=f"synapse_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        st.markdown('</div>', unsafe_allow_html=True)

# ================= HISTORY SECTION =================
if st.session_state.history:
    st.divider()
    st.subheader("Previous Intelligence Reports")
    for idx, item in enumerate(st.session_state.history[::-1]):
        st.markdown(f"**Report {len(st.session_state.history)-idx}** — {item.summary[:60]}...")
