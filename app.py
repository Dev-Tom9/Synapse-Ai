import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from fpdf import FPDF
from datetime import datetime
import io

st.set_page_config(page_title="Synapse Intelligence OS", page_icon="⚡", layout="wide")

st.markdown("""

<style>
.stApp { background-color: #050505; color: #e0e0e0; }
[data-testid="stSidebar"] { background-color: #0c0c0c; border-right: 1px solid #333; }
.stButton>button {
background: linear-gradient(90deg, #00FFA3 0%, #00CCFF 100%);
color: black; font-weight: bold; border: none; width: 100%; height: 3.5rem;
border-radius: 8px;
}
.report-card {
background: rgba(255, 255, 255, 0.02);
padding: 24px; border-radius: 12px; border: 1px solid #222;
border-left: 5px solid #00FFA3;
}
</style>

""", unsafe_allow_html=True)

class IntelligenceReport(BaseModel):
summary: str
key_findings: List[str]
risks: List[str]
strategic_recommendation: str

def create_pdf(data):
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt="SYNAPSE INTELLIGENCE REPORT", ln=True, align='C')
pdf.ln(10)
pdf.set_font("Arial", size=10)
pdf.multi_cell(0, 10, txt=f"Summary: {data.summary}")
return pdf.output(dest='S').encode('latin-1')

with st.sidebar:
st.header("⚡ System Control")
if "api_key" in st.secrets:
api_key = st.secrets["api_key"]
st.success("Engine: Operational")
else:
api_key = st.text_input("Enter Token", type="password")
st.divider()
st.write("Model: GPT-4o")

st.title("Synapse Intelligence OS")
st.caption("AI-Powered Heuristic Extraction Engine")

col1, col2 = st.columns(2)

with col1:
source_text = st.text_area("Input Corpus", height=400)
if st.button("RUN ENGINE"):
if api_key and source_text:
client = OpenAI(api_key=api_key)
with st.spinner("Analyzing..."):
try:
completion = client.beta.chat.completions.parse(
model="gpt-4o",
messages=[{"role": "system", "content": "Extract intelligence."}, {"role": "user", "content": source_text}],
response_format=IntelligenceReport,
)
st.session_state.report = completion.choices[0].message.parsed
except Exception as e:
st.error(f"Error: {e}")

with col2:
if "report" in st.session_state:
rep = st.session_state.report
st.markdown(f'<div class="report-card"><b>Summary:</b>


{rep.summary}</div>', unsafe_allow_html=True)
st.write("### Key Findings")
for f in rep.key_findings:
st.write(f"- {f}")
pdf_bytes = create_pdf(rep)
st.download_button("Download PDF", data=pdf_bytes, file_name="report.pdf")
else:
st.info("System awaiting command...")
