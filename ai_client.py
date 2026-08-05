import os

from dotenv import load_dotenv
from openrouter import OpenRouter

load_dotenv()


def generate_review(code: str, language: str) -> str:
    prompt = f"""You are a senior {language} developer reviewing a code submission.
Review the following code and point out bugs, style issues, and potential problems.
Be concise — use a short bulleted list, no more than 5 points.

Code:
{code}"""

    with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
        response = client.chat.send(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
    return response.choices[0].message.content
