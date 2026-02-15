# ⚡ Synapse Intelligence OS

> Enterprise AI Intelligence & Risk Command Platform

Synapse Intelligence OS is a **production-ready AI web application** built with **Streamlit** and **OpenAI**.  
It transforms unstructured intelligence data (PDF or raw text) into structured insights including **executive summaries, key findings, risk analysis, and strategic recommendations**.

The app demonstrates real-world AI automation, structured output validation, safe file handling, persistent storage, and a professional SaaS-style dashboard.

---

## 🚀 Key Features

- 📄 Upload **one or multiple PDFs** for aggregation
- 📝 Paste raw text for analysis
- 🧠 **AI-powered structured summaries** (or demo mode if no API key)
- 📊 Dynamic **risk severity visualization**
- 📈 **AI confidence indicator**
- 🗂 **Persistent report history** using SQLite
- 💾 Export reports as downloadable **PDFs**
- 🛡 Safe PDF handling (prevents app crashes)
- 🎨 Premium glass-style dashboard
- 🌗 **Theme toggle** (Dark / Light)
- ⚡ Fully responsive layout for **desktop & mobile**

---

## 🧠 AI Output Structure

Reports include:

- **Executive Summary**  
- **Key Findings**  
- **Risk Identification**  
- **Strategic Recommendation**  

If no OpenAI API key is provided or quota is exceeded:

- App switches to **demo mode**
- Generates realistic example reports
- Allows full **dashboard, analytics, and PDF download** functionality

---

## 🏗 Tech Stack

- Python
- Streamlit
- OpenAI API
- Pydantic (structured output validation)
- PyPDF2 (PDF text extraction)
- FPDF (PDF report generation)
- Pandas (analytics & charts)
- SQLite (persistent report storage)

---

## 📦 Installation (Local Setup)

### 1️⃣ Clone Repository

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

### 4️⃣ Run Application

```bash
streamlit run app.py
```

---

## 🔑 API Configuration

You can provide your OpenAI API key in two ways:

### Option 1 — Streamlit Secrets (Recommended for Production)

Create `.streamlit/secrets.toml`:

```toml
api_key = "your_openai_api_key_here"
```

### Option 2 — Sidebar Input

Enter your API key securely during runtime.

> **If you leave it blank or run out of quota**, the app runs fully in **demo mode** with realistic example reports.

---

## ☁ Deployment (Streamlit Cloud)

1. Push repository to GitHub
2. Deploy via Streamlit Cloud
3. Add API key in Streamlit Secrets (optional)
4. Ensure `requirements.txt` includes:

```
streamlit
openai
pydantic
PyPDF2
fpdf
pandas
```

---

## 🛡 Error Handling & Reliability

* Corrupt or unreadable PDFs are safely skipped
* Empty PDFs fall back to manual input
* Missing or exceeded API key triggers **demo mode**
* Persistent SQLite storage preserves report history
* No sensitive data is logged

---

## 📊 Analytics Dashboard

The app includes:

* Risk Score trend over time
* AI Confidence trend over time
* Risk distribution charts
* Historical report access

All analytics work in both **real AI mode** and **demo mode**.

---

## 💰 Cost Consideration

OpenAI API usage costs are billed in USD.
For Nigerian developers:

* ₦1,000 – ₦5,000 worth of credits is enough for demo usage
* Heavy usage depends on model selection and token volume

Monitor usage here:

```
https://platform.openai.com/usage
```

---

## 🔮 Architecture Overview

```
PDF(s) / Text Input
          ↓
Text Aggregation & Preprocessing
          ↓
OpenAI AI Structured Analysis
          ↓
Pydantic Validation & Risk Scoring
          ↓
SQLite Persistent Storage
          ↓
Dashboard Visualization & PDF Export
```

---

## 📈 Future Enhancements

* Multi-user accounts with authentication & roles
* Advanced risk scoring algorithm
* Real-time threat monitoring simulation
* Advanced analytics dashboard filters
* Mobile UI refinements & theme presets

---

## 👨‍💻 Author

**Tomiwa Samuel Otene**
Full Stack Engineer | AI Systems Developer

Demonstrates:

* AI automation
* Structured output engineering
* Persistent storage & session management
* Enterprise dashboard design
* Cloud deployment readiness

---

## 📜 License

This project is for **demonstration, portfolio, and educational purposes**.

```

---

This version:

- Highlights **demo mode** (so you don’t need API credits yet)  
- Shows **all new features** (multi-file, analytics, persistent DB, risk scoring, theme toggle)  
- Professional and interview-ready ✅  
