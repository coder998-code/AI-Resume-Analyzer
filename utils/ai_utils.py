import streamlit as st
from google import genai

client = genai.Client(
    api_key=st.secrets[
        "GEMINI_API_KEY"
    ]
)

@st.cache_data
def is_resume(text):

    resume_check_prompt = f"""
Determine whether this document is a professional resume.

If it is a resume, reply exactly:

RESUME

If not:

NOT_RESUME: <reason>

Document:

{text[:3000]}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=resume_check_prompt
    )

    return response.text.strip()


@st.cache_data
def get_ai_response(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text