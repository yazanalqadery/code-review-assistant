import asyncio
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
            response = await asyncio.wait_for(
                client.chat.send_async(
                    model="openai/gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                ),
                timeout=30.0,
            )
    except asyncio.TimeoutError as e:  # noqa: UP041
        raise RuntimeError(
            "AI review generation timed out after 30 seconds. Please try again later."
        ) from e
    except errors.RateLimitError as e:
        raise RuntimeError(
            "Rate limit exceeded by the AI Provider. Please try again later."
        ) from e
    except errors.UnauthorizedResponseError as e:
        raise RuntimeError(
            "Invalid API key. Please check your OPENROUTER_API_KEY."
        ) from e
    except errors.OpenRouterError as e:
        raise RuntimeError(f"AI Provider API error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error generating review: {e}") from e

    return response.choices[0].message.content


# if __name__ == "__main__":
#     result = asyncio.run(generate_review("def add(a, b):\n    return a+b", "python"))
#     print(result)
