from google import genai
import os

# -------------------------------
# Configure Gemini Client
# -------------------------------

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# -------------------------------
# Generate Cover Letter
# -------------------------------
def generate_cover_letter(
    resume_text,
    job_description,
    resume_data
):

    prompt = f"""
You are an experienced HR recruiter.

Generate a professional cover letter using the following information.

Candidate Name:
{resume_data.get("name", "Candidate")}

Job Description:
{job_description}

Resume:
{resume_text}

Instructions:

- Do NOT use placeholders like [Company Name], [Date], or [Company Address].
- If the company name is not available, use "Hiring Manager".
- Do not invent company details.
- Keep the letter between 200 and 300 words.
- Mention the candidate's relevant skills and projects.
- Explain why the candidate is a good fit for the role.
- End politely using the candidate's name.
- Return only the cover letter text.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"Cover Letter could not be generated.\n{e}"