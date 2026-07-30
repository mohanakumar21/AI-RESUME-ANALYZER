from flask import Flask, render_template, request
import os
from pathlib import Path
import pdfplumber
from docx import Document
from analyzer.skills import extract_skills
from analyzer.parser import parse_resume
from analyzer.ats import calculate_ats_score
from analyzer.suggestions import generate_suggestions

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

    if file.filename == "":
        return "No file selected."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    filename = file.filename.lower()

    if filename.endswith(".pdf"):

        resume_text = extract_pdf_text(filepath)
        skills = extract_skills(resume_text)
        score, missing_skills = calculate_ats_score(skills)
        suggestions = generate_suggestions(score,missing_skills)
        resume_data = parse_resume(resume_text)

    elif filename.endswith(".docx"):

        resume_text = extract_docx_text(filepath)
        skills = extract_skills(resume_text)
        score, missing_skills = calculate_ats_score(skills)
        suggestions = generate_suggestions(score,missing_skills)
        resume_data = parse_resume(resume_text)

    else:

        resume_text = "Unsupported File Format"

    return render_template(
        "results.html",
        resume_text=resume_text,
        skills=skills,
        resume_data=resume_data,
        ats_score=score,
        missing_skills=missing_skills,
        suggestions=suggestions
    )


# -------------------------------
# Run Application
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)