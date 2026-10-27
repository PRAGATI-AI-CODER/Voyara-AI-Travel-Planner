import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


EMBEDDING_MODEL = "models/gemini-embedding-001"


def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=api_key,
    )


def generate_embedding(text: str) -> list[float]:
    """
    Generate a vector embedding for the supplied text.

    The embedding model returns a 3072-dimensional vector
    suitable for storage in the pgvector destination_documents
    table.
    """

    normalized_text = text.strip()

    if not normalized_text:
        raise ValueError(
            "Text cannot be empty."
        )

    client = _get_client()

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=normalized_text,
    )

    if not response.embeddings:
        raise ValueError(
            "Embedding API returned no embeddings."
        )

    embedding = response.embeddings[0].values

    if embedding is None:
        raise ValueError(
            "Embedding API returned an empty vector."
        )

    return list(embedding)