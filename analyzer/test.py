from google import genai

import os

API_KEY = os.getenv("GEMINI_API_KEY")

models = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
]

for model_name in models:
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Say Hello"
        )
        print(f"✅ {model_name} works!")
        print(response.text)
        break
    except Exception as e:
        print(f"❌ {model_name} -> {e}")