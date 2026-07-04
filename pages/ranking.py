import streamlit as st
import sys
import os
import pandas as pd
from io import BytesIO
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from database.db import (
    get_candidates,
    toggle_shortlist,
    get_shortlisted
)


st.set_page_config(
    page_title="Candidate Ranking",
    page_icon="🏆"
)

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

if st.button("⬅ Back to Recruiter Dashboard"):
    st.switch_page("pages/recruiter_dashboard.py")

st.title("Candidate Ranking")

rows = get_candidates()

total_candidates = len(rows)

shortlisted_count = sum(row[6] for row in rows)

average_ats = round(
    sum(row[1] for row in rows) / total_candidates,
    1
)

highest_ats = max(
    row[1] for row in rows
)

if len(rows) == 0:
    st.warning("No candidates found")
    st.stop()

st.subheader("Recruiter Analytics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Candidates",
        total_candidates
    )

with col2:
    st.metric(
        "Shortlisted",
        shortlisted_count
    )

with col3:
    st.metric(
        "Average ATS",
        f"{average_ats}%"
    )

with col4:
    st.metric(
        "Highest ATS",
        f"{highest_ats}%"
    )

st.subheader("What-if Analysis")
st.caption(
    "Adjust the importance of different criteria to instantly see how the candidate ranking changes. "
    "The AI analysis remains the same; only the ranking formula is updated."
)


ats_weight = st.slider(
    "Importance of ATS",
    0,
    10,
    8
)

cgpa_weight = st.slider(
    "Importance of CGPA",
    0,
    10,
    5
)

project_weight = st.slider(
    "Importance of Projects",
    0,
    10,
    7
)

intern_weight = st.slider(
    "Importance of Internship",
    0,
    10,
    5
)

if st.button("Reset Weights"):

    ats_weight = 8
    cgpa_weight = 5
    project_weight = 7
    intern_weight = 5

    st.rerun()

show_shortlisted = st.checkbox(
    "Show only shortlisted candidates"
)

if show_shortlisted:

    rows = [

        row

        for row in rows

        if row[6] == 1

    ]

ranked = []

for r in rows:

    score = (

        r[1] * ats_weight

        +

        r[2] * 10 * cgpa_weight

        +

        r[3] * 10 * project_weight

        +

        r[4] * 10 * intern_weight

    )

    ranked.append({

        "name": r[0],

        "score": score,

        "ats": r[1],

        "cgpa": r[2],

        "projects": r[3],

        "internship": r[4],

        "summary": r[5],

        "shortlisted": r[6]

    })

ranked.sort(
    key=lambda x: x["score"],
    reverse=True
)

st.subheader("Final Ranking")

for i, c in enumerate(ranked):

    with st.expander(f"🏅 Rank {i+1} • {c['name']}"):

        st.metric(
            "⭐ Final Score",
            round(c["score"])
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "ATS",
                c["ats"]
            )

            st.metric(
                "Projects",
                c["projects"]
            )

        with col2:

            st.metric(
                "CGPA",
                c["cgpa"]
            )

            st.metric(
                "Internship",
                c["internship"]
            )

        st.divider()

        st.subheader("📝 AI Summary")

        st.info(c["summary"])

        st.divider()

        if c["shortlisted"]:

            if st.button(
                "✅ Shortlisted",
                key=f"short_{c['name']}"
            ):

                toggle_shortlist(c["name"])

                st.rerun()

        else:

            if st.button(
                "Shortlist",
                key=f"short_{c['name']}"
            ):

                toggle_shortlist(c["name"])

                st.rerun()
    
shortlisted = get_shortlisted()

if shortlisted:

    df = pd.DataFrame(

        shortlisted,

        columns=[

            "Name",

            "ATS",

            "CGPA",

            "Projects",

            "Internship",

            "Summary"

        ]

    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="📥 Download Shortlisted Candidates",

        data=csv,

        file_name="shortlisted_candidates.csv",

        mime="text/csv"

    )

else:

    st.info(

        "No candidates shortlisted yet."

    )

st.markdown("---")
st.caption(
    "🤖 AI Resume Analyzer | Built using Streamlit • Gemini AI • SQLite"
)