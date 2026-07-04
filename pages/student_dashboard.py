import streamlit as st
from pypdf import PdfReader
from PIL import Image
from google import genai
import re
from utils.prompts import *
from utils.pdf_utils import create_pdf
from database.db import create_table
from utils.ai_utils import (
    is_resume,
    get_ai_response
)
from utils.validator import (
    check_resume_sections_ai
)
from utils.parser import (
    extract_score,
    extract_skills,
    extract_missing,
    extract_section_score,
    extract_matched_keywords,
    extract_missing_keywords,
    extract_keyword_percent
)

st.set_page_config(
    page_title="Student Portal",
    page_icon="📄"
)
if st.button("🏠 Home"):
    st.switch_page("app.py")

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

create_table()

client = genai.Client(
    api_key=st.secrets[
        "GEMINI_API_KEY"
    ]
)


st.title("AI Resume Analyzer")

# Upload Resume
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# Analysis Type Selection
analysis_type = st.radio(
    "Select Analysis Type",
    (
        "General Analysis",
        "Analysis with Job Description"
    )
)

job_description = ""

if analysis_type == "Analysis with Job Description":
    job_description = st.text_area(
        "Paste Job Description",
        height=200
    )


# Main Logic
if uploaded_file:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    st.success("Resume uploaded successfully!")

    decision = is_resume(text)

    if not decision.startswith("RESUME"):

        st.error("The uploaded PDF does not appear to be a resume.")

        st.write(decision)

        st.markdown("""
        # ATS Friendly Resume Structure

        ## Contact Information
        Name
        Email
        Phone
        LinkedIn
        GitHub

        ## Professional Summary
        2-3 lines about yourself

        ## Technical Skills
        Programming Languages
        Frameworks
        Databases
        Tools

        ## Education

        ## Projects
        Project Name
        Technologies Used
        Description

        ## Experience

        ## Certifications

        ## Achievements
        """)

        image = Image.open("resume_template.webp")

        st.image(
            image,
            caption="Example Resume Template",
            use_container_width=True
        )

        st.stop()

    sections = check_resume_sections_ai(text)

    st.subheader("Resume Completeness Check")

    for line in sections.split("\n"):

        if ":" not in line:
            continue

        section, status = line.split(":", 1)

        if "YES" in status.upper():

            st.success(f"{section.title()} ✓")

        else:

            st.error(f"{section.title()} ✗")

    # -------------------------------
    # GENERAL ANALYSIS
    # -------------------------------
    if analysis_type == "General Analysis":

        prompt = GENERAL_PROMPT + f"\n\nResume:\n{text}"

    # -------------------------------
    # JD MATCHING
    # -------------------------------
    else:

        if not job_description.strip():
            st.warning("Please paste a Job Description.")
            st.stop()

        prompt = (
            JD_PROMPT
            + f"\n\nJob Description:\n{job_description}"
            + f"\n\nResume:\n{text}"
        )
            

    st.info("Starting AI Analysis...")

    with st.spinner("Analyzing Resume with AI... Please wait"):

        result = get_ai_response(prompt)

    action_match = re.search(
        r"## 30 Day Action Plan(.*?)(?=SKILLS:|$)",
        result,
        re.DOTALL
    )

    display_result = re.sub(
        r"SKILLS:.*",
        "",
        result,
        flags=re.DOTALL
    )

    st.success("AI Analysis Complete!")
               
    score = extract_score(
        result
    )

    skills = extract_skills(
        result
    )

    missing_skills = (
        extract_missing(
            result
        )
    )

    education_score = (
        extract_section_score(
            result,
            "EDUCATION_SCORE"
        )
    )

    skills_score = (
        extract_section_score(
            result,
            "SKILLS_SCORE"
        )
    )

    projects_score = (
        extract_section_score(
            result,
            "PROJECTS_SCORE"
        )
    )

    experience_score = (
        extract_section_score(
            result,
            "EXPERIENCE_SCORE"
        )
    )

    total_score = 0

    if education_score:
        total_score += int(education_score)

    if skills_score:
        total_score += int(skills_score)

    if projects_score:
        total_score += int(projects_score)

    if experience_score:
        total_score += int(experience_score)

    score = extract_score(
        result
    )

    skills = extract_skills(
        result
    )

    missing_skills = (
        extract_missing(
            result
        )
    )

    matched_keywords = (
        extract_matched_keywords(
            result
        )
    )

    missing_keywords = (
        extract_missing_keywords(
            result
        )
    )


    pdf_file = create_pdf(result)
        # ATS Score only for JD Analysis

    if (
            analysis_type == "Analysis with Job Description"
            and score
        ):


            st.metric(
                label="ATS Match Score",
                value=f"{score}%"
                )
    
    percent_match = extract_keyword_percent(
        result
    )

    if (
    analysis_type == "Analysis with Job Description"
    and percent_match
    ):

        st.subheader("Keyword Match")

        st.progress(
            percent_match/ 100
        )

        st.write(
            f"{percent_match}% matched"
        )      
    # Detected Skills

    if skills:

        st.subheader("Detected Skills")

        cols = st.columns(4)

        for i, skill in enumerate(skills):

            cols[i % 4].success(skill)

    # Missing Skills only for JD Analysis

    if (
                analysis_type == "Analysis with Job Description"
                and missing_skills
            ):

                st.subheader("Missing Skills")

                cols = st.columns(4)

                for i, skill in enumerate(missing_skills):

                    cols[i % 4].error(skill)


    if matched_keywords:

        st.subheader("Matched Keywords")

        cols = st.columns(4)

        for i, skill in enumerate(matched_keywords):

            cols[i % 4].success(skill)


    if missing_keywords:

        st.subheader("Missing Keywords")

        cols = st.columns(4)

        for i, skill in enumerate(missing_keywords):

            cols[i % 4].error(skill)
    
    st.subheader("Resume Strength")

    if total_score >= 32:

        st.success(
            f"🟢 Strong Resume ({total_score}/40)"
        )

    elif total_score >= 24:

        st.warning(
                f"🟡 Average Resume ({total_score}/40)"
        )

    else:

        st.error(
            f"🔴 Needs Improvement ({total_score}/40)"
        )
    st.subheader("Resume Section Scores")

    col1, col2 = st.columns(2)

    with col1:

        if education_score:
            st.metric(
                "Education",
                f"{education_score}/10"
            )

        if skills_score:
            st.metric(
                "Skills",
               f"{skills_score}/10"
            )

    with col2:

        if projects_score:
            st.metric(
                "Projects",
                f"{projects_score}/10"
            )

        if experience_score:
            st.metric(
                "Experience",
                f"{experience_score}/10"
            )
    
    if action_match:

        st.subheader("Your 30 Day Improvement Plan")

        st.info(
            action_match.group(1)
        )
    st.subheader("Resume Analysis Report")

    st.markdown(display_result)
    if st.button("Generate 30 Day Improvement Plan"):

        with st.spinner(
            "Generating 30 Day Plan..."
        ):
            plan_prompt = f"""
    You are a career mentor.

    Based on this resume analysis and resume content,
    create a personalized 30 day improvement roadmap.

    Include:

    Week 1:
    Learning goals

    Week 2:
    Project work

    Week 3:
    Resume improvements

    Week 4:
    Application strategy

    Keep tasks realistic.

    Resume Analysis:

    {result}

    Resume:

    {text}
    """
    
            plan = get_ai_response(plan_prompt)

            st.subheader(
                    "Your 30 Day Improvement Plan"
                )

            st.markdown(plan)
    

    with open(pdf_file, "rb") as file:

        st.download_button(
            label="Download Report",
            data=file,
           file_name="resume_analysis_report.pdf",
            mime="application/pdf"
        )

st.markdown("---")
st.caption(
    "🤖 AI Resume Analyzer | Built using Streamlit • Gemini AI • SQLite"
)