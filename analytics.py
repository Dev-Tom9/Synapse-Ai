import pandas as pd
import streamlit as st

def show_analytics(reports):
    if not reports:
        st.info("No reports stored yet.")
        return

    df = pd.DataFrame(reports, columns=[
        "ID", "Summary", "Risks", "Findings",
        "Recommendation", "Risk Score",
        "Confidence", "Created At"
    ])

    st.subheader("📊 Analytics Dashboard")

    st.line_chart(df.set_index("Created At")["Risk Score"])
    st.line_chart(df.set_index("Created At")["Confidence"])

    st.bar_chart(df["Risk Score"])
