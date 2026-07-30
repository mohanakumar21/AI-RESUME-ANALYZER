import re

def extract_job_skills(job_description, skill_database):

    found = []

    job_lower = job_description.lower()

    for skill in skill_database:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, job_lower):

            found.append(skill)

    return sorted(found)


def calculate_match(resume_skills, job_skills):

    matched = []

    missing = []

    for skill in job_skills:

        if skill in resume_skills:

            matched.append(skill)

        else:

            missing.append(skill)

    if len(job_skills) == 0:

        score = 0

    else:

        score = int((len(matched) / len(job_skills)) * 100)

    return score, matched, missing