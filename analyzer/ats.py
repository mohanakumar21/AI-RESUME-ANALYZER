def calculate_ats_score(detected_skills):

    required_skills = [
        "Python",
        "Java",
        "SQL",
        "Git",
        "GitHub",
        "Machine Learning",
        "Flask",
        "AWS",
        "Docker",
        "Linux"
    ]

    found = 0

    missing = []

    for skill in required_skills:

        if skill in detected_skills:
            found += 1
        else:
            missing.append(skill)

    score = int((found / len(required_skills)) * 100)

    return score, missing