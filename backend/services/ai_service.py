import json
import os
import re
import time
from typing import TypeVar

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        timeout=60_000,
    ),
)


GEMINI_MODEL = "gemini-3.1-flash-lite"

MAX_ATTEMPTS = 2
RETRY_DELAYS = (2, 4)


T = TypeVar(
    "T",
    bound=BaseModel,
)


def _generate_content(
    prompt: str,
) -> str:
    """
    Generate normal text using Gemini.

    Gemini structured-output mode is intentionally not used.
    JSON is parsed and validated locally with Pydantic.
    """

    last_error = None

    for attempt in range(MAX_ATTEMPTS):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    automatic_function_calling=(
                        types.AutomaticFunctionCallingConfig(
                            disable=True,
                        )
                    ),
                ),
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response.text

        except Exception as error:
            last_error = error

            if attempt < MAX_ATTEMPTS - 1:
                time.sleep(RETRY_DELAYS[attempt])

    raise RuntimeError(
        "Gemini generation failed after "
        f"{MAX_ATTEMPTS} attempts: {last_error}"
    )


def generate_ai_response(
    prompt: str,
) -> str:
    """
    Generate a normal text response from Gemini.
    """

    return _generate_content(prompt)


def _extract_json_object(
    text: str,
) -> dict:
    """
    Extract a JSON object from Gemini's response.

    Supports:
    - clean JSON
    - Markdown code fences
    - explanatory text surrounding JSON
    """

    cleaned = text.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    try:
        parsed = json.loads(cleaned)

    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise ValueError(
                "Gemini response did not contain a valid JSON object."
            )

        try:
            parsed = json.loads(
                cleaned[start : end + 1]
            )

        except json.JSONDecodeError as error:
            raise ValueError(
                "Gemini returned malformed JSON."
            ) from error

    if not isinstance(parsed, dict):
        raise ValueError(
            "Gemini JSON response must be an object."
        )

    return parsed


def generate_structured_ai_response(
    prompt: str,
    response_schema: type[T],
) -> T:
    """
    Generate JSON using normal Gemini generation and validate
    the result against the supplied Pydantic schema.
    """

    schema_json = json.dumps(
        response_schema.model_json_schema(),
        indent=2,
    )

    structured_prompt = f"""
{prompt}

STRICT OUTPUT FORMAT

Return ONLY one valid JSON object.

Do not use Markdown.
Do not use code fences.
Do not include explanations before or after the JSON.
Do not include fields outside the requested schema.

The required JSON schema is:

{schema_json}

Return the JSON object now.
""".strip()

    last_error = None

    for attempt in range(MAX_ATTEMPTS):
        try:
            raw_response = _generate_content(
                structured_prompt
            )

            parsed_json = _extract_json_object(
                raw_response
            )

            return response_schema.model_validate(
                parsed_json
            )

        except ValueError as error:
            last_error = error

            if attempt < MAX_ATTEMPTS - 1:
                structured_prompt = f"""
{structured_prompt}

CORRECTION REQUIRED

The previous response failed local JSON or Pydantic
validation.

Validation error:
{error}

Generate a completely new response.

Return ONLY valid JSON compatible with the requested schema.
""".strip()

    raise ValueError(
        "Gemini structured generation failed after "
        f"{MAX_ATTEMPTS} attempts: {last_error}"
    )