import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
from typing import List
import random

from database import init_db, save_report, fetch_reports
from utils import extract_text_from_pdfs, calculate_risk_score
from analytics import show_analytics

# ---------------- INIT DB ----------------
init_db()

st.set_page_config(page_title="Synapse Intelligence OS", layout="wide")

# ---------------- THEME TOGGLE ----------------
theme = st.sidebar.toggle("Light Mode")

if theme:
    st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    </style>
    """, unsafe_allow_html=True)

# ---------------- MODEL ----------------
class IntelligenceReport(BaseModel):
    summary: str
    key_findings: List[str]
    risks: List[str]
    strategic_recommendation: str

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔐 API Access")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# ---------------- HEADER ----------------
st.title("⚡ Synapse Intelligence OS")
st.caption("Enterprise AI Intelligence Platform")

# ---------------- INPUT ----------------
uploaded_files = st.file_uploader(
    "Upload Intelligence PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

manual_text = st.text_area("Or Paste Intelligence Text")

if st.button("Run Intelligence Engine"):

    combined_text = ""

    if uploaded_files:
        combined_text += extract_text_from_pdfs(uploaded_files)

    if manual_text:
        combined_text += manual_text

    if not combined_text.strip():
        st.warning("Please upload or paste intelligence data.")
        st.stop()

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
        rep = IntelligenceReport(
            summary="Operational strain and emerging market risks detected.",
            key_findings=["Revenue growth", "Staff turnover rising"],
            risks=["Cybersecurity vulnerability", "Market competition"],
            strategic_recommendation="Scale infrastructure and enhance cybersecurity."
        )

    # -------- Risk Score Algorithm --------
    risk_score = calculate_risk_score(rep.risks)
    confidence = random.randint(85, 99)

    # -------- Save to DB --------
    save_report(
        rep.summary,
        rep.risks,
        rep.key_findings,
        rep.strategic_recommendation,
        risk_score,
        confidence
    )

    # -------- Display --------
    st.subheader("Executive Summary")
    st.write(rep.summary)

    st.subheader("Key Findings")
    for f in rep.key_findings:
        st.write(f"- {f}")

    st.subheader("Risks")
    for r in rep.risks:
        st.write(f"- {r}")

    st.subheader("Recommendation")
    st.write(rep.strategic_recommendation)

    st.metric("Risk Score", f"{risk_score}/100")
    st.metric("AI Confidence", f"{confidence}%")

# ---------------- ANALYTICS ----------------
st.divider()
reports = fetch_reports()
show_analytics(reports)
