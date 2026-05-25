import streamlit as st
from pypdf import PdfReader
import requests
import re

# -------------------------------------------------------------------------
# 1. API CONNECTION AND FALLBACK LOGIC
# -------------------------------------------------------------------------

# Adzuna Free Tier Developer Credentials
ADZUNA_APP_ID = "c08649cc"
ADZUNA_APP_KEY = "04033230a133d18e8a609d17208cfd09"

# Local Fail-Safe Database (Guarantees the app always displays matches if API limits are reached)
LOCAL_BACKUP_JOBS = [
    {
        "title": "Data Scientist (AI & Predictive Analytics)",
        "company": "Nexus Intelligent Systems",
        "location": "Global Remote",
        "description": "Looking for an engineer proficient in Python, Scikit-Learn, and structured SQL. Working on predictive modeling pipelines and refining core datasets.",
        "redirect_url": "https://www.adzuna.com"
    },
    {
        "title": "AI / ML Engineer (Computer Vision Focus)",
        "company": "Kortex Robotics Lab",
        "location": "New York, US / Hybrid",
        "description": "Develop and deploy edge intelligence frameworks using OpenCV, MediaPipe, and YOLO models. Optimization of camera streams and matrix features.",
        "redirect_url": "https://www.adzuna.com"
    },
    {
        "title": "Junior Python Data Analyst",
        "company": "Apex Global Data Corp",
        "location": "London, UK",
        "description": "Entry-to-intermediate role tracking operational metrics. High dependency on clean text processing, Pandas, NumPy, and database triggers.",
        "redirect_url": "https://www.adzuna.com"
    }
]

def fetch_jobs(search_role, country_code="us"):
    """Fetches live listings. Automatically defaults to local mock database on failure."""
    clean_query = requests.utils.quote(search_role.strip())
    url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"
    
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 5,
        "what": clean_query,
        "content-type": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, timeout=6)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results: 
                return results, "Live Server API"
        return LOCAL_BACKUP_JOBS, "Internal Fail-Safe Index (Live API Rate-Limited)"
    except Exception:
        return LOCAL_BACKUP_JOBS, "Internal Fail-Safe Index (Offline Mode)"

# -------------------------------------------------------------------------
# 2. CORE TEXT PROCESSING
# -------------------------------------------------------------------------

def extract_text_from_pdf(file):
    """Safely extracts clear string arrays from standard PDF documents."""
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception:
        return ""

def scan_resume_skills(resume_text):
    """Scans user text against explicit technical data tokens."""
    text_lower = resume_text.lower()
    skill_vocabulary = [
        "python", "machine learning", "data science", "opencv", "mediapipe", 
        "yolo", "sql", "pl/sql", "arduino", "mechatronics", "robotics", 
        "computer vision", "tensorflow", "pytorch", "pandas", "numpy"
    ]
    return [skill.upper() for skill in skill_vocabulary if re.search(r'\b' + re.escape(skill) + r'\b', text_lower)]

# -------------------------------------------------------------------------
# 3. INTERFACE DISPLAY LAYER
# -------------------------------------------------------------------------

st.set_page_config(page_title="Global Job Matcher", page_icon="🌎", layout="centered")

st.title("🌎 Real-Time Global Job Matcher")
st.write("An intermediate application tracking real-time international software positions.")

st.markdown("---")

# User Input Controls
target_role = st.text_input("1. Target Job Title/Keyword", value="Data Scientist")
uploaded_file = st.file_uploader("2. Upload Your Resume (PDF or TXT)", type=["pdf", "txt"])

country = st.selectbox(
    "3. Target Market Region",
    options=[("United States", "us"), ("India", "in"), ("United Kingdom", "gb"), ("Canada", "ca")],
    format_func=lambda x: x[0]
)

if st.button("Search Open Positions Globally", type="primary"):
    if uploaded_file is not None and target_role.strip() != "":
        with st.spinner("Processing document data streams..."):
            
            # Step 1: Read structural text string
            if uploaded_file.name.endswith('.pdf'):
                resume_content = extract_text_from_pdf(uploaded_file)
            else:
                resume_content = str(uploaded_file.read(), "utf-8")
                
            if not resume_content.strip():
                st.error("Error: Could not parse any text from your resume file.")
            else:
                # Step 2: Keywords identification step
                detected_skills = scan_resume_skills(resume_content)
                
                st.subheader("📊 Extracted Profile Highlights")
                if detected_skills:
                    st.success(f"**Identified Core Terms:** {', '.join(detected_skills)}")
                else:
                    st.warning("No explicit technical match terms detected in resume text, evaluating basic title matches...")

                # Step 3: Run the database fetch request
                job_listings, data_source = fetch_jobs(target_role, country_code=country[1])
                
                st.markdown("---")
                st.subheader(f"💼 Openings Found for '{target_role}'")
                st.caption(f"Data Source Pipeline: **{data_source}**")
                
                # Step 4: Render results layout cards with explicit string/dict checking
                for job in job_listings:
                    # Clean out structural bolding tags from API titles
                    title = str(job.get("title", "Job Position")).replace("<strong>", "").replace("</strong>", "")
                    
                    # Safe validation for Company fields (handles mixed API payload data structures)
                    company_data = job.get("company", "Enterprise Corp")
                    if isinstance(company_data, dict):
                        company = company_data.get("display_name", "Enterprise Corp")
                    else:
                        company = str(company_data)
                        
                    # Safe validation for Location fields
                    location_data = job.get("location", "Remote / Hybrid")
                    if isinstance(location_data, dict):
                        location = location_data.get("display_name", "Remote / Hybrid")
                    else:
                        location = str(location_data)
                        
                    description = str(job.get("description", "No description profile provided.")).replace("<strong>", "").replace("</strong>", "")
                    apply_url = job.get("redirect_url", "https://www.adzuna.com")
                    
                    # Score individual listing against detected user keywords
                    match_count = sum(1 for skill in detected_skills if skill.lower() in description.lower())
                    
                    # Display structured output markup container
                    with st.container():
                        st.markdown(f"### 🚀 {title}")
                        st.markdown(f"**🏢 Company:** {company} | **📍 Location:** {location}")
                        st.write(f"*Summary:* {description}")
                        
                        if match_count > 0:
                            st.info(f"✨ Match Factor: Found **{match_count} overlaps** with your current resume competencies.")
                            
                        st.markdown(f"[Apply to this Position]({apply_url})")
                        st.markdown("<hr style='margin:1em 0; border-top:1px dashed #ddd;' />", unsafe_allow_html=True)
                        
    else:
        st.error("Please fill in your target job title and drop a resume format into the dashboard file drop zone.")