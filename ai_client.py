import os

from dotenv import load_dotenv
from openrouter import OpenRouter, errors

load_dotenv()


async def generate_review(code: str, language: str) -> str:
    prompt = f"""You are a senior {language} developer reviewing a code submission.
Review the following code and point out bugs, style issues, and potential problems.
Be concise — use a short bulleted list, no more than 5 points.

Code:
{code}"""
    try:
        async with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
            response = await client.chat.send(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
    except errors.UnauthorizedResponseError:
        raise RuntimeError("Invalid API key. Please check your OPENROUTER_API_KEY.")
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"Error generating review: {e}")

    return response.choices[0].message.content


if __name__ == "__main__":
    result = generate_review("def add(a, b):\n    return a+b", "python")
    print(result)
