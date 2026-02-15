import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from fpdf import FPDF
import io

--- SENIOR UI CONFIG ---
st.set_page_config(page_title="Synapse Intelligence OS", page_icon="⚡", layout="wide")

Injecting Custom CSS for a Mid-Senior "SaaS" Aesthetic
st.markdown("""
<style>
.stApp { background-color: #050505; color: #e0e0e0; }
[data-testid="stSidebar"] { background-color: #0c0c0c; border-right: 1px solid #333; }
.stButton>button {
background: linear-gradient(90deg, #00FFA3 0%, #00CCFF 100%);
color: black; font-weight: bold; border: none; width: 100%; height: 3rem;
border-radius: 8px;
}
.report-card {
background: rgba(255, 255, 255, 0.03);
padding: 24px; border-radius: 12px; border: 1px solid #333;
border-left: 5px solid #00FFA3;
}
.stTabs [data-baseweb="tab-list"] { gap: 10px; }
.stTabs [data-baseweb="tab"] {
background-color: #111; border-radius: 4px 4px 0 0; padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

--- DATA SCHEMA (The "True Extraction" Layer) ---
class IntelligenceReport(BaseModel):
summary: str
key_findings: List[str]
risks: List[str]
strategic_recommendation: str

--- PDF GENERATOR ---
def create_pdf(data):
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt="Synapse AI: Intelligence Report", ln=True, align='C')
pdf.ln(10)

--- MAIN INTERFACE ---
st.title("⚡ Synapse Intelligence OS")
st.caption("Enterprise AI Extraction Engine | Developed by [Your Name]")

with st.sidebar:
st.header("Authentication")
api_key = st.text_input("OpenAI API Key", type="password")
st.divider()
st.markdown("### System Specs")
st.write("- Engine: GPT-4o")
st.write("- Parser: Pydantic v2")
st.info("Verified for high-fidelity data extraction.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
st.subheader("Data Ingestion")
source_text = st.text_area("Paste Corpus Data", height=400, placeholder="Paste reports, logs, or transcripts here...")

with col2:
st.subheader("Intelligence Output")
if "report" in st.session_state:
rep = st.session_state.report
