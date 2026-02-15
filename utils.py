import PyPDF2

def extract_text_from_pdfs(uploaded_files):
    combined_text = ""

    for file in uploaded_files:
        try:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    combined_text += text + "\n"
        except:
            continue

    return combined_text


def calculate_risk_score(risks):
    base_score = len(risks) * 20

    critical_keywords = ["cyber", "breach", "financial", "fraud", "lawsuit"]

    for risk in risks:
        for keyword in critical_keywords:
            if keyword.lower() in risk.lower():
                base_score += 15

    return min(base_score, 100)
