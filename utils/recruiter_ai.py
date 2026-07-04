import re
from google import genai
import streamlit as st


client = genai.Client(

    api_key=st.secrets[
        "GEMINI_API_KEY"
    ]

)


def safe_int(
    value,
    default
):

    try:

        return int(

            str(value)
            .split()[0]

        )

    except:

        return default


def safe_float(
    value,
    default
):

    try:

        return float(

            str(value)
            .split()[0]

        )

    except:

        return default


def analyze_candidates(
    resume_texts,
    job_description
):

    results = []

    for item in resume_texts:

        if isinstance(
            item,
            dict
        ):

            text = item.get(
                "text",
                ""
            )

        else:

            text = str(
                item
            )

        prompt = f"""
You are an experienced technical recruiter.

Your task is to evaluate the candidate's resume
against the given Job Description.

JOB DESCRIPTION:

{job_description}

-----------------------------------

Analyze the resume and return ONLY:

NAME:
ATS:
CGPA:
PROJECTS:
INTERNSHIP:
SUMMARY:

Rules:

ATS -> 0-100 based on JD match

CGPA -> Numeric only

PROJECTS -> Score between 0-10

INTERNSHIP -> Score between 0-10

SUMMARY -> 2-3 sentences explaining
why this candidate fits or doesn't fit
the role.

-----------------------------------

Resume:

{text[:5000]}
"""

        response = (
            client.models.generate_content(

                model="gemini-2.5-flash",

                contents=prompt

            )
        )

        out = response.text


        def extract(
            key,
            default
        ):

            m = re.search(

                rf"{key}\s*:\s*(.*)",

                out

            )

            if m:

                return (
                    m.group(1)
                    .strip()
                )

            return default


        results.append({

            "name":

            extract(
                "NAME",
                "Unknown"
            ),

            "ats":

            safe_int(

                extract(
                    "ATS",
                    50
                ),

                50

            ),

            "cgpa":

            safe_float(

                extract(
                    "CGPA",
                    7
                ),

                7

            ),

            "projects":

            safe_int(

                extract(
                    "PROJECTS",
                    5
                ),

                5

            ),

            "internship":

            safe_int(

                extract(
                    "INTERNSHIP",
                    5
                ),

                5

            ),

            "summary":

            extract(

                "SUMMARY",

                "No summary generated."

            )

        })

    return results