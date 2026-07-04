import streamlit as st
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)
from reportlab.lib.styles import (
    getSampleStyleSheet
)

@st.cache_data
def create_pdf(report_text):

    pdf_file = "resume_report.pdf"

    doc = SimpleDocTemplate(
        pdf_file
    )

    styles = (
        getSampleStyleSheet()
    )

    content = [
        Paragraph(
            report_text.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    ]

    doc.build(content)

    return pdf_file