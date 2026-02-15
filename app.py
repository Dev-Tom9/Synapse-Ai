import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from fpdf import FPDF
from datetime import datetime
import io

# --- SENIOR UI CONFIG ---
st.set_page_config(page_title="Synapse Intelligence OS", page_icon="⚡", layout="wide")

Professional SaaS Theme
st.markdown("""

<style>
.stApp { background-color: #050505; color: #e0e0e0; }
[data-testid="stSidebar"] { background-color: #0c0c0c; border-right: 1px solid #333; }
.stButton>button {
background: linear-gradient(90deg, #00FFA3 0%, #00CCFF 100%);
color: black; font-weight: bold; border: none; width: 100%; height: 3.5rem;
border-radius: 8px; transition: 0.3s;
}
.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0, 255, 163, 0.3); }
.report-card {
background: rgba(255, 255, 255, 0.02);
padding: 24px; border-radius: 12px; border: 1px solid #222;
border-left: 5px solid #00FFA3;
}
</style>

""", unsafe_allow_html=True)

# ------ DATA SCHEMA ---
class IntelligenceReport(BaseModel):
summary: str
key_findings: List[str]
risks: List[str]
strategic_recommendation: str

# --- ENHANCED PDF GENERATOR ---
def create_pdf(data):
pdf = FPDF()
pdf.add_page()
# Header
pdf.set_font("Arial", 'B', 16)
pdf.set_text_color(0, 204, 153) # Brand Color
pdf.cell(200, 10, txt="SYNAPSE INTELLIGENCE REPORT", ln=True, align='C')

# --- SIDEBAR & AUTH ---
with st.sidebar:
st.header("⚡ System Control")

# --- MAIN WORKSPACE ---
st.title("Synapse Intelligence OS")
st.caption("AI-Powered Heuristic Extraction Engine | v4.0 (Senior Build)")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
st.subheader("Data Ingestion")
source_text = st.text_area("Input Corpus", height=450, placeholder="Paste enterprise data here...")

with col2:
st.subheader("Extracted Intelligence")
if "report" in st.session_state:
rep = st.session_state.report
