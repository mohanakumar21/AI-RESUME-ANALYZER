def generate_suggestions(score, missing_skills):

    suggestions = []

    # ATS score based suggestions
    if score < 50:
        suggestions.append(
            "Your ATS score is low. Add more relevant technical skills."
        )

    elif score < 80:
        suggestions.append(
            "Good resume. Adding a few more industry skills can improve it."
        )

    else:
        suggestions.append(
            "Excellent ATS score. Keep your resume updated."
        )

    # Missing skill suggestions
    for skill in missing_skills:

        if skill == "SQL":
            suggestions.append(
                "Learn SQL to strengthen database knowledge."
            )

        elif skill == "Docker":
            suggestions.append(
                "Docker knowledge improves deployment skills."
            )

        elif skill == "AWS":
            suggestions.append(
                "AWS Cloud is highly valued by recruiters."
            )

        elif skill == "GitHub":
            suggestions.append(
                "Add GitHub projects to showcase your coding work."
            )

        elif skill == "Java":
            suggestions.append(
                "Learning Java improves placement opportunities."
            )

        elif skill == "Linux":
            suggestions.append(
                "Linux is an important skill for software engineers."
            )

        elif skill == "Flask":
            suggestions.append(
                "Flask helps you build Python web applications."
            )

        elif skill == "Machine Learning":
            suggestions.append(
                "Machine Learning skills strengthen AI profiles."
            )

        elif skill == "Python":
            suggestions.append(
                "Python is one of the most important programming languages."
            )

        else:
            suggestions.append(
                f"Consider learning {skill}."
            )

    return suggestions