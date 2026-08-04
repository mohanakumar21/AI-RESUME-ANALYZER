def get_achievements(reports):

    achievements = []

    total_reports = len(reports)

    if total_reports >= 1:

        achievements.append({
            "icon":"🥉",
            "title":"First Resume",
            "description":"Analyzed your first resume."
        })

    if total_reports >= 10:

        achievements.append({
            "icon":"🥈",
            "title":"Resume Expert",
            "description":"Analyzed 10 resumes."
        })

    highest_ats = 0

    highest_match = 0

    for report in reports:

        if report.ats_score > highest_ats:
            highest_ats = report.ats_score

        if report.match_score > highest_match:
            highest_match = report.match_score

    if highest_ats >= 90:

        achievements.append({

            "icon":"🥇",

            "title":"ATS Master",

            "description":"Reached ATS Score above 90."

        })

    if highest_match >= 80:

        achievements.append({

            "icon":"🎯",

            "title":"Job Match Pro",

            "description":"Reached Job Match above 80%."

        })

    if total_reports >= 20:

        achievements.append({

            "icon":"🚀",

            "title":"Resume Champion",

            "description":"Analyzed 20 resumes."

        })

    return achievements