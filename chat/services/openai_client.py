from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def test_openai_connection():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Explain what a SQL JOIN is in one sentence."
            }
        ]
    )
    return response.choices[0].message.content
