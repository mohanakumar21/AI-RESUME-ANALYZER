from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    filename,
    resume_data,
    ats_score,
    skills,
    missing_skills,
    suggestions,
    roadmap,
    match_score,
    matched_skills,
    missing_job_skills,
    ai_feedback,
    cover_letter
):

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(filename)

    story = []

    # -----------------------------
    # Title
    # -----------------------------

    story.append(
        Paragraph("<b>AI Resume Analysis Report</b>", styles["Title"])
    )

    story.append(Spacer(1,20))
    story.append(
    Paragraph(
        f"<b>Generated on:</b> {datetime.now().strftime('%d %b %Y %I:%M %p')}",
        styles["BodyText"]
    )
    )

    story.append(Spacer(1,20))

    # -----------------------------
    # Candidate
    # -----------------------------

    story.append(
        Paragraph("<b>Candidate Information</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(f"Name : {resume_data.get('name','Not Found')}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Email : {resume_data.get('email','Not Found')}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"Phone : {resume_data.get('phone','Not Found')}", styles["BodyText"])
    )

    story.append(Spacer(1,15))

    # -----------------------------
    # ATS
    # -----------------------------

    story.append(
        Paragraph("<b>ATS Score</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(f"{ats_score}/100", styles["BodyText"])
    )

    story.append(Spacer(1,15))

    # -----------------------------
    # Skills
    # -----------------------------

    story.append(
        Paragraph("<b>Detected Skills</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            ", ".join(skills) if skills else "No skills detected.",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,15))

    # -----------------------------
    # Missing Skills
    # -----------------------------

    story.append(
        Paragraph("<b>Missing Skills</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
              ", ".join(missing_skills) if missing_skills else "No missing skills.",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,15))

    # -----------------------------
    # Suggestions
    # -----------------------------

    story.append(
        Paragraph("<b>AI Suggestions</b>", styles["Heading2"])
    )

    for item in suggestions:

        story.append(
            Paragraph(f"• {item}", styles["BodyText"])
        )

    story.append(Spacer(1,15))

# -----------------------------
# Roadmap
# -----------------------------

    story.append(
        Paragraph("<b>Resume Improvement Roadmap</b>", styles["Heading2"])
    )

    for item in roadmap:

        story.append(
            Paragraph(f"• {item}", styles["BodyText"])
        )

    story.append(Spacer(1,15))
    # -----------------------------
    # Job Match
    # -----------------------------

    story.append(
        Paragraph("<b>Job Match Score</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(f"{match_score}%", styles["BodyText"])
    )

    story.append(Spacer(1,15))

    story.append(
        Paragraph(
            ", ".join(matched_skills) if matched_skills else "No matching skills found.",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            ", ".join(missing_job_skills) if missing_job_skills else "No missing job skills.",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,15))


    # -----------------------------
    # AI Review
    # -----------------------------

    story.append(
        Paragraph("<b>AI Resume Review</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(ai_feedback.replace("\n","<br/>"), styles["BodyText"])
    )

    story.append(Spacer(1,15))

    # -----------------------------
    # Cover Letter
    # -----------------------------

    story.append(
        Paragraph("<b>AI Cover Letter</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(cover_letter.replace("\n","<br/>"), styles["BodyText"])
    )

    doc.build(story)