import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from fpdf import FPDF
from datetime import datetime

st.set_page_config(
    page_title="Synapse Intelligence OS",
    page_icon="⚡",
    layout="wide"
)

# ================= UI =================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #0e1117, #050505 70%);
    color: #f3f4f6;
    font-family: 'Inter', sans-serif;
}
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 20px;
}
.stButton>button {
    background: linear-gradient(90deg, #00FFA3, #00CCFF);
    color: black;
    font-weight: 700;
    border-radius: 14px;
    height: 3rem;
    border: none;
}
textarea {
    background-color: #111827 !important;
    border-radius: 16px !important;
    border: 1px solid #1f2937 !important;
    color: white !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================= MODEL =================
class IntelligenceReport(BaseModel):
    summary: str
    key_findings: List[str]
    risks: List[str]
    strategic_recommendation: str

# ================= SIDEBAR =================
with st.sidebar:
    st.header("⚡ System Access")

    if "api_key" in st.secrets:
        api_key = st.secrets["api_key"]
        st.success("Secure Key Loaded")
    else:
        api_key = st.text_input("Enter OpenAI API Key", type="password")

# ================= HERO =================
st.markdown("""
<div class="glass-card">
<h1>⚡ Synapse Intelligence OS</h1>
<p>Strategic AI Intelligence & Risk Profiling Engine</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# ================= INPUT =================
with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    source_text = st.text_area("Input Intelligence Corpus", height=350)
    run = st.button("Run Intelligence Engine")
    st.markdown('</div>', unsafe_allow_html=True)

# ================= OUTPUT =================
with col2:
    if run:
        if not api_key:
            st.error("API Key Missing.")
        elif not source_text:
            st.warning("Please enter text.")
        else:
            try:
                client = OpenAI(api_key=api_key)

                with st.spinner("Analyzing Intelligence..."):
                    completion = client.beta.chat.completions.parse(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "Extract structured intelligence."},
                            {"role": "user", "content": source_text}
                        ],
                        response_format=IntelligenceReport,
                    )

                rep = completion.choices[0].message.parsed

                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("Executive Summary")
                st.write(rep.summary)

                st.subheader("Key Findings")
                for f in rep.key_findings:
                    st.write(f"- {f}")

                st.subheader("Risks")
                for r in rep.risks:
                    st.write(f"- {r}")

                st.subheader("Strategic Recommendation")
                st.write(rep.strategic_recommendation)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Engine Failure: {e}")
