import re

SKILLS_DATABASE = [
    "Python",
    "Java",
    "C",
    "C++",
    "Flask",
    "Django",
    "Git",
    "GitHub",
    "Linux",
    "SQL",
    "MySQL",
    "MongoDB",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "OpenCV",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "Google Cloud",
    "REST API",
    "FastAPI",
    "NumPy",
    "Pandas",
    "Scikit-learn"
]


def extract_skills(resume_text):

    found_skills = []

    resume_lower = resume_text.lower()

    for skill in SKILLS_DATABASE:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, resume_lower):

            found_skills.append(skill)

    return sorted(found_skills)