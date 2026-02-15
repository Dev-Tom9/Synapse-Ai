import sqlite3
from datetime import datetime

DB_NAME = "synapse.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary TEXT,
            risks TEXT,
            findings TEXT,
            recommendation TEXT,
            risk_score INTEGER,
            confidence INTEGER,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_report(summary, risks, findings, recommendation, risk_score, confidence):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO reports
        (summary, risks, findings, recommendation, risk_score, confidence, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        summary,
        ",".join(risks),
        ",".join(findings),
        recommendation,
        risk_score,
        confidence,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def fetch_reports():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM reports ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows
