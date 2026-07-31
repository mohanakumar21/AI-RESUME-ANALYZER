from google import genai

API_KEY = "YOUR_API_KEY"

client = genai.Client(api_key=API_KEY)

models = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
    "gemini-3.5-pro"
]

for model in models:
    try:
        response = client.models.generate_content(
            model=model,
            contents="Say Hello"
        )
        print(f"✅ {model} works")
        print(response.text)
        break

    except Exception as e:
        print(f"❌ {model} -> {e}")