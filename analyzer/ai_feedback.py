from google import genai

# -------------------------------
# Configure Gemini Client
# -------------------------------

import os

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)


# -------------------------------
# Generate AI Feedback
# -------------------------------

def generate_ai_feedback(
    resume_text,
    ats_score,
    missing_skills,
    match_score
):

    prompt = f"""
You are an experienced HR recruiter and ATS expert.

Analyze the following resume.

ATS Score: {ats_score}/100

Job Match Score: {match_score}%

Missing Skills:
{", ".join(missing_skills)}

Resume:

{resume_text}

Return the response in plain text only.

Do NOT use Markdown.

Do NOT use **bold**, *, #, or numbered lists.

Use exactly this format:

Strengths:
- Point 1
- Point 2
- Point 3

Weaknesses:
- Point 1
- Point 2
- Point 3

Suggestions:
- Point 1
- Point 2
- Point 3 """

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"AI Feedback could not be generated.\n{e}"