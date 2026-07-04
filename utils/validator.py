from utils.ai_utils import get_ai_response

def check_resume_sections_ai(text):

    prompt = f"""
You are an ATS resume reviewer.

Determine whether the following sections are present in the resume.

Consider alternative headings as valid.

Examples:
Academic Background = Education
Work History = Experience
Technical Skills = Skills

Return EXACTLY in this format:

EDUCATION: YES/NO
SKILLS: YES/NO
PROJECTS: YES/NO
EXPERIENCE: YES/NO
CERTIFICATIONS: YES/NO

Resume:

{text}
"""
    return get_ai_response(prompt)
