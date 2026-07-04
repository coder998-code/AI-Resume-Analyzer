import streamlit as st
import sys
import os
from database.db import (

    save_candidate,

    clear_candidates,

    create_table

)
from utils.ai_utils import (
    is_resume
)

sys.path.append(

    os.path.dirname(

        os.path.dirname(

            os.path.abspath(
                __file__
            )

        )

    )

)

from utils.recruiter_resume_loader import (
    load_resumes
)

from utils.recruiter_ai import (
    analyze_candidates
)

st.set_page_config(
    page_title="Recruiter Dashboard",
    page_icon="👨‍💼"
)

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

if st.button("🏠 Home"):
    st.switch_page("app.py")

def show_recruiter():

    create_table()

    st.title("Recruiter Dashboard")
    st.subheader(
        "Job Description"
    )

    job_description = st.text_area(
        "Paste the Job Description",
        height=200,
        placeholder="Paste the company's JD here..."
    )

    st.subheader(
        "Recruitment Preferences"
    )

    uploaded_resumes = st.file_uploader(

        "Upload Candidate Resumes",

        type=["pdf"],

        accept_multiple_files=True

    )

    resume_texts = []

    if uploaded_resumes:

        resume_texts = load_resumes(
            uploaded_resumes
        )

        valid_resumes = []

        skipped = []
        for resume in resume_texts:

            decision = is_resume(
                resume["text"]
            )

            if decision.startswith("RESUME"):

                valid_resumes.append(
                    resume
                )

            else:

                skipped.append(
                    resume["name"]
                )
        
        st.success(
            f"{len(valid_resumes)} valid resumes loaded"
        )

        if skipped:

            st.warning(
                "Skipped non-resume files:"
            )

            for file in skipped:

                st.write(f"❌ {file}")

    ats_weight = st.slider(

        "ATS Score",

        0,

        10,

        8

    )

    cgpa_weight = st.slider(

        "CGPA",

        0,

        10,

        5

    )

    project_weight = st.slider(

        "Projects",

        0,

        10,

        7

    )

    intern_weight = st.slider(

        "Internship Experience",

        0,

        10,

        6

    )

    candidate_results = []

    if st.button(
        "Analyze Candidates"
    ):

        if not valid_resumes:

            st.warning(
                "Upload resumes first."
            )

        else:

            with st.spinner(
                "Analyzing resumes..."
            ):
                clear_candidates()

                candidate_results = analyze_candidates(
                    valid_resumes,
                    job_description
                )
                st.write(
                    resume_texts
                )

                st.write(
                    candidate_results
                )

                for candidate in candidate_results:

                    save_candidate(

                        candidate

                    )


                st.success(

                    "Analysis Complete"

                )


                st.write(

                    f"{len(candidate_results)} candidates saved"

                )


                st.switch_page(

                    "pages/ranking.py"

                )

            st.subheader(
                "Candidate Ranking"
            )

            for c in candidate_results:

                c["final"] = (

                    c["ats"]
                    * ats_weight

                    +

                    c["cgpa"]
                    * 10
                    * cgpa_weight

                    +

                    c["projects"]
                    * 10
                    * project_weight

                    +

                    c["internship"]
                    * 10
                    * intern_weight

                )

            ranked = sorted(

                candidate_results,

                key=lambda x:
                x["final"],

                reverse=True

            )

            for i, c in enumerate(
                ranked
            ):

                with st.expander(

                    f"#{i+1} {c['name']}"

                ):

                    st.metric(

                        "Final Score",

                        round(
                            c["final"]
                        )

                    )

                    st.write(
                        "ATS:",
                        c["ats"]
                    )

                    st.write(
                        "CGPA:",
                        c["cgpa"]
                    )

                    st.write(
                        "Projects:",
                        c["projects"]
                    )

                    st.write(
                        "Internship:",
                        c["internship"]
                    )

st.markdown("---")
st.caption(
    "🤖 AI Resume Analyzer | Built using Streamlit • Gemini AI • SQLite"
)
# REMOVE THIS LATER
#show_recruiter()