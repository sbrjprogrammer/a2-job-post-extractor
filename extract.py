
import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError

from schema import Extracted


# Project configuration
BASE_DIR = Path(__file__).resolve().parent
PROMPT_PATH = BASE_DIR / "prompts" / "extract.txt"
MAX_ATTEMPTS = 3


def extract_with_retry(client, model, prompt, job_text):
    """
    Extract job information using Gemini.
    Retry up to 3 times if Pydantic validation fails.
    """

    current_prompt = f"""
{prompt}

Job posting:
{job_text}
"""

    for attempt in range(1, MAX_ATTEMPTS + 1):

        try:
            # Call Gemini API
            response = client.models.generate_content(
                model=model,
                contents=current_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=Extracted,
                ),
            )

            if not response.text:
                raise ValueError("Model returned an empty response.")

            # Validate response using Pydantic
            result = Extracted.model_validate_json(response.text)

            # Return valid extracted data
            return result

        except ValidationError as error:

            print(
                f"Validation failed on attempt {attempt}: {error}",
                file=sys.stderr,
            )

            # Stop after 3 failed attempts
            if attempt == MAX_ATTEMPTS:
                raise RuntimeError(
                    "Extraction failed after 3 attempts."
                ) from error

            # Send validation error back to Gemini
            current_prompt += f"""

Your previous response failed validation.

Validation error:
{error}

Please correct the response and return valid JSON
matching the Extracted schema.

Do not repeat the previous validation mistake.
"""


def main():

    # Read input from command line
    parser = argparse.ArgumentParser(
        description="Extract structured information from job postings."
    )

    parser.add_argument(
        "text",
        help="Messy job posting text to extract information from."
    )

    args = parser.parse_args()

    # Load environment variables
    load_dotenv(BASE_DIR / ".env")

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")

    # Validate configuration
    if not api_key:
        print(
            "Error: GEMINI_API_KEY is missing in .env",
            file=sys.stderr,
        )
        sys.exit(1)

    if not model:
        print(
            "Error: GEMINI_MODEL is missing in .env",
            file=sys.stderr,
        )
        sys.exit(1)

    # Check prompt file
    if not PROMPT_PATH.exists():
        print(
            "Error: prompts/extract.txt not found.",
            file=sys.stderr,
        )
        sys.exit(1)

    prompt = PROMPT_PATH.read_text(encoding="utf-8")

    try:
        # Initialize Gemini client
        client = genai.Client(api_key=api_key)

        # Extract information with retry mechanism
        result = extract_with_retry(
            client,
            model,
            prompt,
            args.text,
        )

        # Print only valid JSON to stdout
        print(result.model_dump_json(indent=2))

    except Exception as error:

        # Send errors to stderr, not stdout
        print(
            f"Extraction failed: {error}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
