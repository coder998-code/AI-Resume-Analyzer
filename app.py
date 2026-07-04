import streamlit as st


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
st.title("🤖 AI Resume Analyzer")

st.markdown(
    """
### AI-powered Resume Analysis & Recruitment Platform

Analyze resumes, improve ATS scores, rank candidates, and streamline hiring with AI.

---
"""
)

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Resume Analyzer")

st.markdown(
    """
Welcome!

Choose your role to continue.
"""
)

col1, col2 = st.columns(2)

with col1:

    st.subheader("👨‍🎓 Student")

    st.write(
        """
Analyze your resume

• ATS Score

• Resume Feedback

• Skill Gap Analysis

• 30-Day Improvement Plan
        """
    )

    if st.button(
        "Open Student Portal",
        use_container_width=True
    ):

        st.switch_page(
            "pages/student_dashboard.py"
        )

with col2:

    st.subheader("👨‍💼 Recruiter")

    st.write(
        """
Upload multiple resumes

• Candidate Ranking

• AI Candidate Summary

• Shortlisting

• CSV Export
        """
    )

    if st.button(
        "Open Recruiter Portal",
        use_container_width=True
    ):

        st.switch_page(
            "pages/recruiter_dashboard.py"
        )

st.markdown("---")

st.caption(
    "Built using Streamlit • Gemini AI • SQLite"
)