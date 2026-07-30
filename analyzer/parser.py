import re


# -----------------------------
# Extract Name
# -----------------------------
IGNORE_KEYWORDS = [
    "university",
    "college",
    "institute",
    "school",
    "department",
    "email",
    "phone",
    "mobile",
    "contact",
    "skills",
    "projects",
    "education",
    "experience",
    "objective",
    "summary",
    "linkedin",
    "github",
    "b.tech",
    "b.e",
    "m.tech",
    "resume"
]


def extract_name(text):

    lines = text.split("\n")

    # First Priority: Look for "Name:"
    for line in lines:

        clean = line.strip()

        if clean.lower().startswith("name:"):
            return clean.split(":", 1)[1].strip()

    # Second Priority: Detect capitalized names
    for line in lines:

        line = line.strip()

        if line == "":
            continue

        lower = line.lower()

        if any(keyword in lower for keyword in IGNORE_KEYWORDS):
            continue

        if "@" in line:
            continue

        if re.search(r"\d{6,}", line):
            continue

        words = line.split()

        if 2 <= len(words) <= 4:

            if all(word[0].isupper() for word in words):
                return line

    return "Not Found"


# -----------------------------
# Extract Email
# -----------------------------
def extract_email(text):

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


# -----------------------------
# Extract Phone
# -----------------------------
def extract_phone(text):

    pattern = r"(\+91[\-\s]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


# -----------------------------
# Extract Education
# -----------------------------
def extract_education(text):

    education_keywords = [
        "b.tech",
        "b.e",
        "m.tech",
        "m.e",
        "b.sc",
        "m.sc",
        "bca",
        "mca",
        "bachelor",
        "master"
    ]

    lines = text.split("\n")

    for line in lines:

        lower = line.lower()

        if any(keyword in lower for keyword in education_keywords):
            return line.strip()

    return "Not Found"


# -----------------------------
# Extract Experience
# -----------------------------
def extract_experience(text):

    pattern = r"(\d+)\+?\s*(years|year|yrs|yr)"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group()

    return "Fresher"


# -----------------------------
# Extract Projects
# -----------------------------
def extract_projects(text):

    projects = []

    lines = text.split("\n")

    capture = False

    for line in lines:

        clean = line.strip()

        if clean.lower() == "projects":
            capture = True
            continue

        if capture:

            if clean == "":
                break

            projects.append(clean)

    return projects


# -----------------------------
# Parse Resume
# -----------------------------
def parse_resume(text):

    return {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "education": extract_education(text),

        "experience": extract_experience(text),

        "projects": extract_projects(text)

    }