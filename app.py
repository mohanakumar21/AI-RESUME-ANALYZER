from flask import Flask, render_template, request, send_file
import os
from pathlib import Path
import pdfplumber
from docx import Document
from analyzer.parser import parse_resume
from analyzer.ats import calculate_ats_score
from analyzer.suggestions import generate_suggestions
from analyzer.job_match import extract_job_skills, calculate_match
from analyzer.skills import extract_skills, SKILLS_DATABASE
from analyzer.ai_feedback import generate_ai_feedback
from analyzer.roadmap import generate_roadmap
from analyzer.cover_letter import generate_cover_letter
from analyzer.pdf_generator import generate_pdf



latest_report ={}


# -------------------------------
# Project Configuration
# -------------------------------

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)

UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)

# -------------------------------
# PDF Text Extraction
# -------------------------------

def extract_pdf_text(path):
    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# -------------------------------
# DOCX Text Extraction
# -------------------------------

def extract_docx_text(path):
    doc = Document(path)

    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text


# -------------------------------
# Home Page
# -------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# Resume Upload
# -------------------------------

@app.route("/upload", methods=["POST"])
def upload():

    if "resume" not in request.files:
        return "No file uploaded."

    file = request.files["resume"]
    job_description = request.form.get("job_description", "")


    if file.filename == "":
        return "No file selected."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    filename = file.filename.lower()

    if filename.endswith(".pdf"):

        # Extract resume text
        resume_text = extract_pdf_text(filepath)

    elif filename.endswith(".docx"):

        # Extract resume text
        resume_text = extract_docx_text(filepath)

    else:

        return "Unsupported File Format"

    # ---------------- Resume Analysis ----------------

    skills = extract_skills(resume_text)

    resume_data = parse_resume(resume_text)

    score, missing_skills = calculate_ats_score(skills)

    suggestions = generate_suggestions(score, missing_skills)
    roadmap = generate_roadmap(missing_skills)

    # ---------------- Job Matching ----------------

    job_skills = extract_job_skills(job_description)  
    match_score, matched_skills, missing_job_skills = calculate_match(
        skills,
        job_skills
    )
    ai_feedback = generate_ai_feedback(
        resume_text,
        score,
        missing_skills,
        match_score
    )    
    cover_letter = generate_cover_letter(
       resume_text,
        job_description,
        resume_data
    )

    latest_report["resume_data"] = resume_data
    latest_report["ats_score"] = score
    latest_report["skills"] = skills
    latest_report["missing_skills"] = missing_skills
    latest_report["suggestions"] = suggestions
    latest_report["roadmap"] = roadmap
    latest_report["match_score"] = match_score
    latest_report["matched_skills"] = matched_skills
    latest_report["missing_job_skills"] = missing_job_skills
    latest_report["ai_feedback"] = ai_feedback
    latest_report["cover_letter"] = cover_letter

    return render_template(
        "results.html",
        resume_text=resume_text,
        skills=skills,
        resume_data=resume_data,
        ats_score=score,
        missing_skills=missing_skills,
        suggestions=suggestions,
        roadmap=roadmap,
        job_description=job_description,
        job_skills=job_skills,
        match_score=match_score,
        matched_skills=matched_skills,
        missing_job_skills=missing_job_skills,
        ai_feedback=ai_feedback,
        cover_letter=cover_letter,
    )

@app.route("/download")
def download():

    filename = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "Resume_Report.pdf"
    )

    generate_pdf(
        filename,
        latest_report["resume_data"],
        latest_report["ats_score"],
        latest_report["skills"],
        latest_report["missing_skills"],
        latest_report["suggestions"],
        latest_report["roadmap"],
        latest_report["match_score"],
        latest_report["matched_skills"],
        latest_report["missing_job_skills"],
        latest_report["ai_feedback"],
        latest_report["cover_letter"]
    )

    return send_file(
        filename,
        as_attachment=True
    )
    # -------------------------------
    # Run Application
    # -------------------------------
if __name__ == "__main__":

    app.run(debug=True)