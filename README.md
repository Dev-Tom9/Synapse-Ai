# ⚡ Synapse Intelligence OS

> Enterprise AI Intelligence & Risk Command Platform

Synapse Intelligence OS is a production-ready AI web application built with **Streamlit** and **OpenAI**.  
It transforms unstructured intelligence data (PDF or raw text) into structured executive insights including summaries, key findings, risk analysis, and strategic recommendations.

This project demonstrates real-world AI automation, structured output engineering, safe file handling, and SaaS-style dashboard design.

---

## 🚀 Live Features

- 📄 Upload intelligence reports in PDF format
- 📝 Paste raw intelligence text
- 🧠 AI-powered structured analysis
- 📊 Dynamic risk severity visualization
- 📈 AI confidence indicator
- 🗂 Session-based report history
- 📥 Export structured reports as downloadable PDFs
- 🛡 Safe PDF error handling (prevents crashes)
- 🎨 Premium glass-style enterprise dashboard UI

---

## 🧠 AI Output Structure

The system extracts and formats intelligence into:

- Executive Summary
- Key Findings
- Risk Identification
- Strategic Recommendation

Structured output is validated using **Pydantic models** to ensure consistent, production-grade formatting.

If no API key is provided or quota is exceeded, the system automatically switches to a safe fallback demo mode.

---

## 🏗 Tech Stack

- Python
- Streamlit
- OpenAI API
- Pydantic
- PyPDF2
- FPDF
- Pandas

---

## 📦 Installation (Local Setup)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/synapse-ai.git
cd synapse-ai
````

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 🔑 API Configuration

You can provide your OpenAI API key in two ways:

### Option 1 — Streamlit Secrets (Recommended for Production)

Create:

```
.streamlit/secrets.toml
```

Add:

```toml
api_key = "your_openai_api_key_here"
```

### Option 2 — Sidebar Input

Enter your API key securely in the app sidebar during runtime.

---

## ☁ Deployment (Streamlit Cloud)

1. Push repository to GitHub
2. Deploy via Streamlit Cloud
3. Add API key in Streamlit Secrets
4. Ensure `requirements.txt` contains:

```
streamlit
openai
pydantic
PyPDF2
fpdf
pandas
```

---

## 🛡 Production-Level Error Handling

* Corrupt or unreadable PDFs are safely handled
* Empty PDF text automatically falls back to manual input
* API quota errors trigger safe demo mode
* Session state preserves report history
* No sensitive information is logged

---

## 💰 Cost Consideration

OpenAI API usage costs are billed in USD.

For Nigerian developers:

* ₦1,000 – ₦5,000 worth of API credits is sufficient for demo usage.
* Heavy usage depends on model selection and token volume.

Always monitor usage at:

```
https://platform.openai.com/usage
```

---

## 📊 Application Architecture

```
User Input (PDF / Text)
        ↓
Safe Parsing Layer
        ↓
OpenAI Structured Analysis
        ↓
Pydantic Validation
        ↓
Dashboard Visualization + PDF Export
```

---

## 📈 Future Improvements

* Multi-file intelligence aggregation
* Persistent database storage
* Authentication & role-based access
* Risk scoring algorithm refinement
* Real-time threat monitoring
* Theme switch (Dark / Light)
* Advanced analytics dashboard

---

## 👨‍💻 Author

**Samuel Otene**
Full Stack Engineer | AI Systems Developer

This project demonstrates:

* AI automation
* Structured response engineering
* Production-ready error handling
* Cloud deployment readiness
* Modern SaaS dashboard UI design

---

## 📜 License

This project is built for demonstration, portfolio, and educational purposes.

```

---

This is now:

✅ Proper GitHub Markdown  
✅ Clean structure  
✅ Developer-friendly  
✅ Professional tone  
✅ Includes ₦ reference  
✅ Interview-ready  
