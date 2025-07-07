'''# app.py (Updated with Dark Theme Toggle and Loader)

import streamlit as st
import os
import time
from resume_parser.parser import parse_resume
from job_dataset.processor import load_and_process_job_data
from recommender.matcher import match_resume_to_jobs

# ==== Page Config ====
st.set_page_config(page_title="AI Job Recommender", layout="centered")

# ==== Dark Theme Toggle ====
dark_mode = st.toggle("🌙 Dark Mode")

# ==== Inject CSS ====
css_light = """
    <style>
        body { background-color: #f5f7fa; }
        .main-title { font-size: 3em; font-weight: 800; text-align: center; color: #0a66c2; }
        .subheader { font-size: 1.2em; margin-top: 1rem; color: #444; }
        .job-card { background-color: #fff; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .job-title { font-size: 1.2em; font-weight: 600; color: #0a66c2; }
        .score { font-size: 1em; color: #333; }
        .resume-section { background-color: #fff; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
"""

css_dark = """
    <style>
        body { background-color: #1e1e1e; color: #eee; }
        .main-title { font-size: 3em; font-weight: 800; text-align: center; color: #61dafb; }
        .subheader { font-size: 1.2em; margin-top: 1rem; color: #ccc; }
        .job-card { background-color: #2a2a2a; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(255,255,255,0.05); }
        .job-title { font-size: 1.2em; font-weight: 600; color: #61dafb; }
        .score { font-size: 1em; color: #eee; }
        .resume-section { background-color: #2a2a2a; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(255,255,255,0.05); }
    </style>
"""

st.markdown(css_dark if dark_mode else css_light, unsafe_allow_html=True)

# ==== Title ====
st.markdown('<div class="main-title">AI Job Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Upload your resume and discover the best IT job roles tailored to your skills </p>', unsafe_allow_html=True)

# ==== Upload ====
uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file:
    resume_path = os.path.join("resumes", uploaded_file.name)
    with open(resume_path, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("🔍 Parsing your resume and loading jobs..."):
        time.sleep(1)  # simulate loading
        skills_path = "data/skills.csv"
        parsed_resume = parse_resume(resume_path, skills_path)

        if parsed_resume:
            st.success("✅ Resume Parsed Successfully!")
            st.markdown('<div class="resume-section">', unsafe_allow_html=True)
            st.write("**Name:**", parsed_resume["name"])
            st.write("**Email:**", parsed_resume["email"])
            st.write("**Phone:**", parsed_resume["phone"])
            st.write("**Skills Extracted:**", ", ".join(parsed_resume["skills"]))
            st.markdown('</div>', unsafe_allow_html=True)

            # Load job data
            job_path = "data/full_it_job_dataset.csv"
            df, tfidf_matrix, vectorizer, kmeans_model = load_and_process_job_data(job_path)

            # Match jobs
            min_score = st.slider("📊 Minimum Match Score (%)", 0, 100, 15, step=1)
            show_description = st.toggle("📝 Show Job Description")

            matches = match_resume_to_jobs(parsed_resume["skills"], df, tfidf_matrix, vectorizer, kmeans_model)
            filtered_matches = [job for job in matches if job["score"] >= min_score]

            st.subheader("🎯 Top Matching Jobs")
            if filtered_matches:
                for job in filtered_matches:
                    st.markdown(f"""
                        <div class="job-card">
                            <div class="job-title">{job['title']}</div>
                            <div class="score">Match Score: <b>{job['score']}%</b></div>
                            {"<div style='margin-top:0.5rem; font-size:0.9em;'>"+ job['description'] +"</div>" if show_description and job.get("description") else ""}
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ No jobs match your criteria. Try lowering the threshold.")
        else:
            st.error("❌ Failed to parse resume.")'''

# app.py

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import os
from resume_parser.parser import parse_resume
from job_dataset.processor import load_and_process_job_data
from recommender.matcher import match_resume_to_jobs

# ========== Page Config ==========
st.set_page_config(page_title="AI Job Recommender", layout="wide")
# ======= Load and Display Logo =======
logo_path = os.path.join("asserts", "logo.png")
if os.path.exists(logo_path):
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(
            """
            <div style='text-align: center;'>
                <img src='https://raw.githubusercontent.com/KISHORE-KANNA-07/Skill-Horizon/main/asserts/logo.png' 
                    style='width: 120px; height: 120px; border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.2);' />
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("<h1 style='margin-bottom: 0;'>Skill-Horizon</h1>", unsafe_allow_html=True)
        st.markdown("<p style='margin-top: -8px; color: gray;'>Expand Your Potential to New Horizons</p>", unsafe_allow_html=True)
else:
    st.warning("⚠️ Logo file not found. Please check the path.")
# ========== Theme Toggle ==========
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    dark_mode = st.toggle("🌙 Dark Mode", key="dark-mode-toggle")

# ========== Custom Theme and Styles ==========
st.markdown(f"""
    <style>
        :root {{
            --bg-light: #f5f7fa;
            --bg-dark: #1e1e1e;
            --text-light: #000000;
            --text-dark: #ffffff;
            --primary-light: #0a66c2;
            --primary-dark: #66b2ff;
            --card-bg-light: #ffffff;
            --card-bg-dark: #2b2b2b;
            --shadow-light: rgba(0, 0, 0, 0.1);
            --shadow-dark: rgba(0, 0, 0, 0.4);
        }}

        html, body {{
            background-color: var(--bg-{ 'dark' if dark_mode else 'light' });
            color: var(--text-{ 'dark' if dark_mode else 'light' });
        }}

        .main-title {{
            font-size: 2.8em;
            font-weight: 800;
            text-align: center;
            color: var(--primary-{ 'dark' if dark_mode else 'light' });
            margin-top: 0.5rem;
        }}

        .subheader {{
            font-size: 1.2em;
            text-align: center;
            margin-bottom: 1.5rem;
            color: var(--card-{ 'dark' if dark_mode else 'light' });
        }}

        .resume-section, .job-card {{
            background-color: var(--card-bg-{ 'dark' if dark_mode else 'light' });
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1.2rem;
            box-shadow: 0 4px 6px var(--shadow-{ 'dark' if dark_mode else 'light' });
            transition: transform 0.2s ease;
        }}

        .job-card:hover {{
            transform: translateY(-3px);
        }}

        .job-title {{
            font-size: 1.3em;
            font-weight: 700;
            color: var(--primary-{ 'dark' if dark_mode else 'light' });
        }}

        .score-bar-container {{
            background-color: #f0f0f0;
            border-radius: 6px;
            height: 10px;
            margin-top: 8px;
            overflow: hidden;
        }}

        .score-bar {{
            height: 100%;
            transition: width 0.4s ease;
            border-radius: 6px;
            background-color: var(--primary-{ 'dark' if dark_mode else 'light' });
        }}

        .score-text {{
            margin-top: 6px;
            font-size: 0.95em;
            color: var(--text-{ 'dark' if dark_mode else 'light' });
        }}

        .container {{
            max-width: 900px;
            margin: auto;
            padding: 0 1rem;
        }}
    </style>
""", unsafe_allow_html=True)



# ========== Title and Header ==========
st.markdown(f"<div class='container'><div class='main-title'>💼 AI Job Recommendation System</div>" +
            f"<p class='subheader'>Upload your resume and discover the best IT job roles tailored to your skills 🚀</p></div>", unsafe_allow_html=True)

# ========== Upload Section ==========
uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file:
    os.makedirs("resumes", exist_ok=True)  # ✅ Ensures the folder exists
    resume_path = os.path.join("resumes", uploaded_file.name)
    with open(resume_path, "wb") as f:
        f.write(uploaded_file.read())


    skills_path = "data/skills.csv"
    parsed_resume = parse_resume(resume_path, skills_path)

    if parsed_resume:
        st.success("✅ Resume Parsed Successfully!")
        st.markdown("<div class='resume-section container'>", unsafe_allow_html=True)
        st.write("**Name:**", parsed_resume["name"])
        st.write("**Email:**", parsed_resume["email"])
        st.write("**Phone:**", parsed_resume["phone"])
        st.write("**Skills Extracted:**", ", ".join(parsed_resume["skills"]))
        st.markdown("</div>", unsafe_allow_html=True)

        job_path = "data/full_it_job_dataset.csv"
        df, tfidf_matrix, vectorizer, kmeans_model = load_and_process_job_data(job_path)

        min_score = st.slider("📊 Minimum Match Score (%)", 0, 100, 15, step=1)
        show_description = st.toggle("📝 Show Job Description")
        with st.spinner("🔍 Matching your resume to relevant job roles..."):
            matches = match_resume_to_jobs(parsed_resume["skills"], df, tfidf_matrix, vectorizer, kmeans_model)
        filtered_matches = [job for job in matches if job["score"] >= min_score]
        
        # Auto-scroll JavaScript
        components.html("""
            <script>
                const jobResults = document.getElementById("job-results");
                if (jobResults) {
                    jobResults.scrollIntoView({ behavior: 'smooth' });
                }
            </script>
        """, height=0)

        st.markdown('<div id="job-results"></div>', unsafe_allow_html=True)
        st.subheader("🎯 Top Matching Jobs")

        if filtered_matches:
            for job in filtered_matches:
                score_color = f"linear-gradient(to right, #4caf50 {job['score']}%, #e0e0e0 {job['score']}%)"
                st.markdown(f"""
                    <div class="job-card">
                        <div class="job-title">{job['title']}</div>
                        <div class="score-text">Match Score: <b>{job['score']}%</b></div>
                        <div class="score-bar-container">
                            <div class="score-bar" style="width: {job['score']}%; background: {score_color};"></div>
                        </div>
                        {"<div style='margin-top:0.7rem; font-size:0.9em; color:#888;'>"+ job['description'] +"</div>" if show_description and job.get("description") else ""}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No jobs match your criteria. Try lowering the threshold.")

    else:
        st.error("❌ Failed to parse resume.")
