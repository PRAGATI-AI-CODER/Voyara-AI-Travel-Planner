import os
import time
from typing import TypeVar

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")


client = genai.Client(api_key=GEMINI_API_KEY)


GEMINI_MODELS = [
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
]


T = TypeVar("T", bound=BaseModel)


def generate_ai_response(prompt: str) -> str:
    last_error = None

    for model in GEMINI_MODELS:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                if not response.text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return response.text

            except Exception as error:
                last_error = error

                if "503" not in str(error):
                    raise

                time.sleep(2 ** attempt)

    raise RuntimeError(
        f"Gemini models are temporarily unavailable: {last_error}"
    )


def generate_structured_ai_response(
    prompt: str,
    response_schema: type[T],
) -> T:
    last_error = None

    for model in GEMINI_MODELS:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=response_schema,
                    ),
                )

                if not response.text:
                    raise RuntimeError(
                        "Gemini returned an empty structured response."
                    )

                return response_schema.model_validate_json(
                    response.text
                )

            except Exception as error:
                last_error = error

                if "503" not in str(error):
                    raise

                time.sleep(2 ** attempt)

    raise RuntimeError(
        f"Gemini structured generation is temporarily unavailable: "
        f"{last_error}"
    )