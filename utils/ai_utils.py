import streamlit as st
from google import genai

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
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

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=resume_check_prompt
        )

        return response.text.strip()

    except Exception as e:

        error = str(e)

        if "429" in error:

            st.error(
                "🚦 Gemini API rate limit reached.\n\nPlease wait about a minute and try again."
            )

        elif "503" in error:

            st.error(
                "🔧 Gemini service is temporarily unavailable.\n\nPlease try again in a few moments."
            )

        else:

            st.error(
                f"Unexpected error:\n\n{error}"
            )

        if st.button("🔄 Retry"):
            st.rerun()

        st.stop()


@st.cache_data
def get_ai_response(prompt):

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        error = str(e)

        if "429" in error:

            st.error(
                "🚦 Gemini API rate limit reached.\n\nPlease wait about a minute and try again."
            )

        elif "503" in error:

            st.error(
                "🔧 Gemini service is temporarily unavailable.\n\nPlease try again in a few moments."
            )

        else:

            st.error(
                f"Unexpected error:\n\n{error}"
            )

        if st.button("🔄 Retry"):
            st.rerun()

        st.stop()