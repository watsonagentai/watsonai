import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from logs_config import get_logger

logger = get_logger(__name__)

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


def interpret_histogram(histogram: dict) -> str:
    if not API_KEY:
        logger.error("No OPENAI_API_KEY set. Cannot call OpenAI.")
        return "No interpretation available."

    # Construct the new OpenAI client
    client = OpenAI(api_key=API_KEY)

    # Convert histogram dict to JSON for passing to the prompt
    histogram_json = json.dumps(histogram, indent=2)

    # Our system and user prompts:
    system_prompt = (
        "You are a helpful AI that produces a professional, structured user profile summary.\n"
        "You may optionally use ANSI color codes (e.g. \\x1b[33m for yellow) in the text.\n"
        "You can handle a histogram of up to 100 or more categories.\n"
        "If there are many categories, you may cluster or group them before summarizing.\n"
        "Output should be plain text."
    )

    # We encourage the AI to consider large category histograms gracefully
    user_prompt = f"""
We have a histogram of categories for a user's online presence, potentially with many categories:

{histogram_json}

Please produce a summary with these sections:

1) Overall Summary
   - A short introduction describing the user's probable interests/online presence.
2) Key Categories
   - If there are many categories, group or cluster them, then highlight the top categories.
3) Potential Interests
   - Based on the categories, speculate on user interests, but mark them as speculation.
4) Additional Notes
   - Mention any observations or disclaimers.

Keep it concise but informative. You may use color codes (e.g. \\x1b[92m for bright green) to emphasize parts.
Remember: the user might have 100+ categories, so do not just list them all one by one. Summarize or group them if needed.
    """

    logger.info("Sending data to OpenAI (openai) for interpretation...")

    try:
        # Use the new library approach: client.chat.completions.create(...)
        response = client.chat.completions.create(
            model="gpt-4o",  # Example placeholder model name
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )

        # In newer openai libraries, the result is an object with attribute access:
        # Typically: response.choices[0].message.content
        # This avoids the "object is not subscriptable" error.
        if not response.choices:
            logger.error("OpenAI returned no choices.")
            return "No choices returned by OpenAI."

        first_choice = response.choices[0]
        content = first_choice.message.content if first_choice.message else ""
        logger.info("Received a completion from OpenAI.")

        # Some versions store request_id in different ways; check your library version.
        # This might be .request_id or ._request_id (private). If unavailable, omit it.
        req_id = getattr(response, "request_id", None) or getattr(response, "_request_id", None)
        if req_id:
            logger.info(f"OpenAI Request ID: {req_id}")

        return content.strip() if content else ""

    except Exception as e:
        logger.error(f"OpenAI call failed: {e}")
        return f"Error calling OpenAI: {e}"
