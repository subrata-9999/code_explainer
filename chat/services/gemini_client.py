import requests
from django.conf import settings

# GEMINI_URL = (
#     "https://generativelanguage.googleapis.com/v1beta/"
#     "models/gemini-1.5-flash:generateContent"
# )

def extract_text_from_gemini(data: dict):
    try:
        candidates = data.get("candidates")
        if not candidates:
            return None

        content = candidates[0].get("content")
        if not content:
            return None

        parts = content.get("parts")
        if not parts:
            return None

        return parts[0].get("text")

    except Exception:
        return None

def test_gemini_connection():
    text = explain_with_gemini(
        "Explain what a SQL JOIN is in one sentence."
    )

    return text or "Gemini did not return a response"


GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-flash-latest:generateContent"
)

def explain_with_gemini(prompt: str):
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={settings.GEMINI_API_KEY}",
            json=payload,
            timeout=30
        )

        data = response.json()
        print("RAW GEMINI RESPONSE:", data)

        return extract_text_from_gemini(data)

    except Exception as e:
        print("Gemini request failed:", e)
        return None
