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
    layout="wide"
)

# ===============================
# CUSTOM STYLING (PREMIUM UI)
# ===============================
st.markdown("""
<style>

/* === GLOBAL === */
.stApp {
    background: linear-gradient(135deg, #050505, #0e1117);
    color: #e6edf3;
    font-family: 'Segoe UI', sans-serif;
}

/* === SIDEBAR === */
[data-testid="stSidebar"] {
    background: #0b0f14;
    border-right: 1px solid #1f2937;
}

/* === HEADINGS === */
h1 {
    font-size: 42px !important;
    font-weight: 700 !important;
    letter-spacing: -1px;
}

h3 {
    color: #00FFA3 !important;
}

/* === BUTTON === */
.stButton>button {
    background: linear-gradient(90deg, #00FFA3 0%, #00CCFF 100%);
    color: black;
    font-weight: 600;
    border: none;
    width: 100%;
    height: 3rem;
    border-radius: 12px;
    transition: 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.03);
    box-shadow: 0px 0px 20px rgba(0, 255, 163, 0.5);
}

/* === TEXT AREA === */
textarea {
    background-color: #0f172a !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #1e293b !important;
}

/* === REPORT CARD === */
.report-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    padding: 30px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

/* === DOWNLOAD BUTTON === */
.stDownloadButton>button {
    background: #111827;
    color: #00FFA3;
    border: 1px solid #00FFA3;
    border-radius: 12px;
}

.stDownloadButton>button:hover {
    background: #00FFA3;
    color: black;
}

/* === SCROLLBAR === */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #00FFA3;
    border-radius: 10px;
}

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
# SIDEBAR
# ===============================
with st.sidebar:
    st.header("⚡ System Control")

    if "api_key" in st.secrets:
        api_key = st.secrets["api_key"]
        st.success("Engine: Operational")
    else:
        api_key = st.text_input("Enter OpenAI Token", type="password")

    st.divider()
    st.write("Model: GPT-4o")


# ===============================
# MAIN HEADER
# ===============================
st.markdown("""
<h1>⚡ Synapse Intelligence OS</h1>
<p style='color:#9ca3af; font-size:18px;'>
AI-Powered Strategic Intelligence Extraction Engine
</p>
""", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2)


# ===============================
# INPUT SECTION
# ===============================
with col1:
    source_text = st.text_area("Input Intelligence Corpus", height=400)

    if st.button("RUN ENGINE"):
        if api_key and source_text:
            client = OpenAI(api_key=api_key)

            with st.spinner("Analyzing Intelligence..."):
                try:
                    completion = client.beta.chat.completions.parse(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "Extract structured intelligence."},
                            {"role": "user", "content": source_text}
                        ],
                        response_format=IntelligenceReport,
                    )

                    st.session_state.report = completion.choices[0].message.parsed

                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please provide API key and input text.")


# ===============================
# OUTPUT SECTION
# ===============================
with col2:
    if "report" in st.session_state:
        rep = st.session_state.report

        st.markdown(
            f"""
            <div class="report-card">
                <h3>Executive Summary</h3>
                <p>{rep.summary}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 🔍 Key Findings")
        for f in rep.key_findings:
            st.markdown(f"- {f}")

        st.markdown("### ⚠ Risk Factors")
        for r in rep.risks:
            st.markdown(f"- {r}")

        st.markdown("### 🎯 Strategic Recommendation")
        st.markdown(f"**{rep.strategic_recommendation}**")

        pdf_bytes = create_pdf(rep)

        st.download_button(
            "Download Intelligence Report (PDF)",
            data=pdf_bytes,
            file_name=f"synapse_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

    else:
        st.info("System awaiting command...")
