def generate_roadmap(missing_skills):

    roadmap = []

    week = 1

    skill_plan = {

        "Python": [
            "Complete Python OOP",
            "Solve 20 Python problems"
        ],

        "Java": [
            "Learn Core Java",
            "Build one Java Mini Project"
        ],

        "SQL": [
            "Learn SQL Basics",
            "Practice 25 SQL Queries"
        ],

        "Flask": [
            "Build a Flask CRUD Application",
            "Understand Routing & Templates"
        ],

        "Docker": [
            "Install Docker",
            "Containerize your Flask Project"
        ],

        "AWS": [
            "Learn AWS Cloud Basics",
            "Deploy a Flask App on AWS"
        ],

        "GitHub": [
            "Improve GitHub README",
            "Upload 3 Quality Projects"
        ],

        "Linux": [
            "Learn Linux Commands",
            "Practice Shell Scripting"
        ],

        "Machine Learning": [
            "Complete ML Basics",
            "Build one ML Project"
        ],

        "Deep Learning": [
            "Learn Neural Networks",
            "Build a CNN Project"
        ]
    }

    for skill in missing_skills:

        if skill in skill_plan:

            roadmap.append({

                "week": week,

                "skill": skill,

                "tasks": skill_plan[skill]

            })

            week += 1

    return roadmap