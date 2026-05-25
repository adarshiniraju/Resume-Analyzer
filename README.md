# 🌎 Real-Time Global Job Matcher

A sleek, intermediate-level Python web application built with **Streamlit** that extracts technical competencies from an uploaded resume and matches them against active, real-time job openings from around the world using the Adzuna Global Aggregator API. 

The application features a robust type-checking data pipeline and an integrated offline fail-safe mechanism to guarantee high-availability performance even under API rate limits.

---

## 🚀 Features

- **Automated Resume Parsing:** Extracts plain text formatting out of multi-page binary PDF and TXT documents.
- **Skill Extraction Engine:** Analyzes resume content structures against an industry-standard technical vocabulary matrix (Python, Machine Learning, Core Databases, Computer Vision, etc.).
- **Live Global Pipeline:** Queries active job markets (US, UK, India, Canada) directly through remote API connections.
- **Robust Error Handling:** Features safe data-structure validation (`isinstance`) to parse unpredictable nested API responses without crashing.
- **Offline Fail-Safe:** Automatically switches over to an internal indexed mockup database if external servers drop requests or exceed developer rate thresholds.

---

## 📥 Installation & Setup

### 1. Install Required Dependencies
Open your terminal and run the following command to install the required external library environments:
```bash
pip install streamlit pypdf requests
streamlit run job_match.py
