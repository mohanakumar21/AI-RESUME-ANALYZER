# 🤖 AI Resume Analyzer

An AI-powered Resume Analyzer built with **Flask**, **Python**, and **Google Gemini AI** that evaluates resumes using ATS (Applicant Tracking System) scoring, skill extraction, job description matching, AI-generated resume reviews, cover letter generation, and downloadable PDF reports.

---

# 🚀 Features

### 📄 Resume Analysis
- ✅ Upload Resume (PDF & DOCX)
- ✅ Resume Parsing
- ✅ ATS Compatibility Score
- ✅ Resume Preview
- ✅ Skill Extraction
- ✅ Missing Skill Detection
- ✅ AI Resume Suggestions

### 🎯 Job Matching
- ✅ Job Description Analysis
- ✅ Job Match Score
- ✅ Matching Skills
- ✅ Missing Job Skills

### 🤖 AI Features
- ✅ AI Resume Review using Google Gemini
- ✅ AI Cover Letter Generator
- ✅ Personalized Resume Improvement Roadmap

### 📊 Analytics Dashboard
- ✅ ATS Score Doughnut Chart
- ✅ Job Match Doughnut Chart
- ✅ Animated Score Counters
- ✅ Interactive Dashboard

### 📑 Reports
- ✅ Download Complete Resume Analysis as PDF

### 🎨 User Interface
- ✅ Responsive Design
- ✅ Modern Dashboard
- ✅ Loading Animation
- ✅ Smooth UI Animations

---

# 📸 Screenshots

## 🏠 Home Page

<img width="100%" src="Screenshots/home.png">

---

## 📊 Resume Analysis

<img width="100%" src="Screenshots/result.png">

---

## 🤖 AI Resume Review

<img width="100%" src="Screenshots/ai_feedback.png">

---

## 📈 Analytics Dashboard

<img width="100%" src="Screenshots/dashboard.png">

---

## 📄 PDF Report

<img width="100%" src="Screenshots/pdf_report.png">

---

# 🛠 Tech Stack

## Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js

## Backend
- Python
- Flask

## Artificial Intelligence
- Google Gemini API
- Prompt Engineering

## Resume Processing
- pdfplumber
- python-docx
- Regular Expressions (Regex)

## PDF Generation
- ReportLab

## Version Control
- Git
- GitHub

---

# 📂 Project Structure

```
AI-RESUME-ANALYZER
│
├── analyzer/
│   ├── parser.py
│   ├── ats.py
│   ├── skills.py
│   ├── suggestions.py
│   ├── job_match.py
│   ├── ai_feedback.py
│   ├── roadmap.py
│   ├── cover_letter.py
│   └── pdf_generator.py
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── results.css
│
├── templates/
│   ├── index.html
│   └── results.html
│
├── uploads/
├── app.py
├── requirements.txt
└── README.md
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/mohanakumar21/AI-RESUME-ANALYZER.git
```

```bash
cd AI-RESUME-ANALYZER
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Gemini API

Create an environment variable:

```
GEMINI_API_KEY
```

Add your Google Gemini API Key.

---

## Run the Application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

# 📊 Current Capabilities

- Resume Parsing
- ATS Score Calculation
- Skill Extraction
- Missing Skill Detection
- AI Resume Suggestions
- Job Description Matching
- AI Resume Review
- AI Cover Letter Generation
- Resume Improvement Roadmap
- Interactive Analytics Dashboard
- Download PDF Report

---

# 🚀 Future Improvements

- User Authentication
- Resume History
- Resume Templates
- Resume Comparison
- Resume Ranking
- AI Resume Rewrite
- Multi-Resume Analysis
- Cloud Deployment (Render/Railway)

---

# 📚 Learning Outcomes

This project helped me learn:

- Flask Web Development
- Python Backend Development
- Resume Parsing
- ATS Scoring Logic
- Google Gemini API Integration
- Prompt Engineering
- PDF Report Generation
- Interactive Dashboard Development
- HTML, CSS & JavaScript
- Chart.js
- Git & GitHub Workflow

---

# 👨‍💻 Author

**Mohanakumar S**

B.Tech – Electronics and Computer Engineering

VIT Chennai

### GitHub

https://github.com/mohanakumar21

### LinkedIn

https://www.linkedin.com/in/mohanakumar21/

---

# ⭐ Support

If you found this project useful:

⭐ Star this repository

🍴 Fork this repository

💬 Share your feedback

---

## 📌 Project Status

**Version:** v1.5

**Status:** Active Development

**Completed:** Milestones 1–15 ✅

**Next:** User Authentication & Resume History (Milestone 16)