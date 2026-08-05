from flask import Flask, render_template, request, send_file,flash,url_for
from flask_mail import Mail, Message
from flask import flash, redirect, url_for
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
from database import db
from models import User, ResumeHistory
from flask_login import LoginManager
from werkzeug.security import (generate_password_hash,check_password_hash)
from flask import redirect
from flask_login import (LoginManager,login_user,logout_user,login_required,current_user)
from datetime import datetime
from flask_login import current_user
from analyzer.achievements import get_achievements


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
app.config["SECRET_KEY"] = "your_secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(BASE_DIR / "resume.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# ---------------- Mail Configuration ----------------

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "mohanakumar2106@gmail.com"
app.config["MAIL_PASSWORD"] = "wwqa lmsq lkcx flhx"
app.config["MAIL_DEFAULT_SENDER"] = "mohanakumar2106@gmail.com"

mail = Mail(app)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
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
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("register"))

@app.route("/analyze")
@login_required
def analyze():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("register.html",error="Email already registered. Please login or use another email.")

        password = generate_password_hash(
            request.form["password"]
        )

        user = User(

            username=username,

            email=email,

            password=password

        )

        db.session.add(user)

        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        # User not found
        if user is None:
            return render_template(
                "login.html",
                error="Invalid Email or Password"
            )

        # Correct password
        if check_password_hash(user.password, password):
            login_user(user)
            flash("Login Successful!", "success")
            return redirect(url_for("dashboard"))

        # Wrong password
        return render_template(
            "login.html",
            error="Invalid Email or Password"
        )

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")
# -------------------------------
# Resume Upload
# -------------------------------

@app.route("/upload", methods=["POST"])
def upload():

    if "resume" not in request.files:
        return "No file uploaded."

    file = request.files["resume"]
    job_description = request.form.get("job_description", "")
    print("===== JOB DESCRIPTION =====")
    print(job_description)
    print("===========================")


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
    history = ResumeHistory(

    resume_name=file.filename,

    filename="Resume_Report.pdf",

    ats_score=score,

    match_score=match_score,

    created_at=datetime.now(),

    pdf_path="Resume_Report.pdf",

    user_id=current_user.id

    )

    db.session.add(history)
    db.session.commit()
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
    print("Latest report keys:", latest_report.keys())

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
        ai_feedback = ai_feedback.replace(". ", ".\n\n"),
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
@app.route("/send-email")
@login_required
def send_email():

    if not latest_report:
        return "Please analyze a resume before sending the email."

    filename = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "Resume_Report.pdf"
    )

    # Always generate the latest PDF
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

    recipient = latest_report["resume_data"].get("email")

    if not recipient or recipient == "Not Found":
        return "Email address not found in resume."

    msg = Message(
        subject="Your AI Resume Analysis Report",
        sender=app.config["MAIL_USERNAME"],
        recipients=[recipient]
    )

    msg.body = (
        "Hello,\n\n"
        "Please find your AI Resume Analysis Report attached.\n\n"
        "Thank you for using AI Resume Analyzer."
    )

    with app.open_resource(filename) as fp:
        msg.attach(
            "Resume_Report.pdf",
            "application/pdf",
            fp.read()
        )

    mail.send(msg)

   

    flash("✅ Report emailed successfully!", "success")
    return redirect(url_for("dashboard"))
    
@app.route("/history")
@login_required
def history():

    reports = ResumeHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(
        ResumeHistory.created_at.desc()
    ).all()

    return render_template(
        "history.html",
        history=reports
    )


@app.route("/dashboard")
@login_required
def dashboard():

    reports = ResumeHistory.query.filter_by(
        user_id=current_user.id
    ).limit(5).all()

    total_reports = len(reports)

    if total_reports > 0:

        average_ats = sum(r.ats_score for r in reports) / total_reports

        highest_ats = max(r.ats_score for r in reports)

        latest = reports[-1].created_at

    else:

        average_ats = 0
        highest_ats = 0
        latest = None
    if total_reports > 0:
        average_match = round(sum(r.match_score for r in reports) / total_reports)
        latest_resume = reports[-1].resume_name

    else:
        average_match = 0
        latest_resume = "No Resume"
    return render_template(
        "dashboard.html",
        reports=reports,
        total_reports=total_reports,
        average_ats=round(average_ats),
        highest_ats=highest_ats,
        latest=latest,
        average_match=average_match,
        latest_resume=latest_resume
    )
@app.route("/profile")
@login_required
def profile():

    reports = ResumeHistory.query.filter_by(
        user_id=current_user.id
    ).all()
    achievements = get_achievements(reports)

    total_reports = len(reports)

    if total_reports:

        average_ats = round(
            sum(r.ats_score for r in reports) / total_reports
        )

        highest_ats = max(r.ats_score for r in reports)

        average_match = round(
            sum(r.match_score for r in reports) / total_reports
        )

    else:

        average_ats = 0
        highest_ats = 0
        average_match = 0

    return render_template(
        "profile.html",
        total_reports=total_reports,
        average_ats=average_ats,
        highest_ats=highest_ats,
        average_match=average_match,
        achievements=achievements
    )
@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip()

        # Validation

        if not username or not email:

            flash("All fields are required.", "danger")
            return redirect(url_for("edit_profile"))

        # Check duplicate username

        existing_user = User.query.filter(
            User.username == username,
            User.id != current_user.id
        ).first()

        if existing_user:

            flash("Username already exists.", "danger")
            return redirect(url_for("edit_profile"))

        # Check duplicate email

        existing_email = User.query.filter(
            User.email == email,
            User.id != current_user.id
        ).first()

        if existing_email:

            flash("Email already exists.", "danger")
            return redirect(url_for("edit_profile"))

        current_user.username = username
        current_user.email = email

        db.session.commit()

        flash("Profile updated successfully!", "success")

        return redirect(url_for("profile"))

    return render_template("edit_profile.html")
    
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":

        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        # Check current password

        if not check_password_hash(
            current_user.password,
            current_password
        ):

            flash("Current password is incorrect.", "danger")
            return redirect(url_for("change_password"))

        # Check new passwords match

        if new_password != confirm_password:

            flash("New passwords do not match.", "danger")
            return redirect(url_for("change_password"))

        # Optional: Minimum password length

        if len(new_password) < 8:

            flash(
                "Password must be at least 8 characters long.",
                "danger"
            )
            return redirect(url_for("change_password"))

        # Save new password

        current_user.password = generate_password_hash(new_password)

        db.session.commit()

        flash("Password updated successfully!", "success")

        return redirect(url_for("profile"))

    return render_template("change_password.html")
    
  
    
    # -------------------------------
    # Run Application
    # -------------------------------
if __name__ == "__main__":

    app.run(debug=True)