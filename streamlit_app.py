import streamlit as st
from openai import OpenAI

# 1. Page Config
st.set_page_config(page_title="Synapse AI", page_icon="🧠", layout="wide")

# 2. Sidebar for API Key
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.info("Get a key at platform.openai.com")

# 3. Main UI
st.title("🧠 Synapse AI: Executive Intelligence")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    user_input = st.text_area("Paste complex text or reports here:", height=300)
    analyze_button = st.button("Generate Intelligence Report", use_container_width=True)

with col2:
    if analyze_button:
        if not api_key:
            st.warning("Please enter your API Key in the sidebar!")
        elif not user_input:
            st.warning("Please paste some text first!")
        else:
            client = OpenAI(api_key=api_key)
            with st.spinner("Decoding content..."):
                # The "Strong" Prompt
                prompt = f"Analyze this text and provide: 1. A 3-sentence executive summary. 2. The detected emotional tone. 3. Three 'Hidden Opportunities' or 'Actionable Risks'. Text: {user_input}"
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                report = response.choices[0].message.content
                st.success("Analysis Complete")
                st.markdown(report)
