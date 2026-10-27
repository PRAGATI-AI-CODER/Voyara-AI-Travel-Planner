from dataclasses import dataclass

from database.database import SessionLocal
from database.rag_models import DestinationDocument
from services.embedding_service import generate_embedding


DEFAULT_TOP_K = 3


@dataclass
class RetrievedChunk:
    destination: str
    title: str
    content: str
    source: str
    chunk_index: int
    similarity: float


def retrieve_destination_chunks(
    destination: str,
    query: str,
    top_k: int = DEFAULT_TOP_K,
) -> list[RetrievedChunk]:
    """
    Retrieve the most relevant destination knowledge chunks
    using pgvector cosine similarity.
    """

    normalized_destination = destination.strip()
    normalized_query = query.strip()

    if not normalized_destination:
        raise ValueError(
            "Destination cannot be empty."
        )

    if not normalized_query:
        raise ValueError(
            "Query cannot be empty."
        )

    if top_k < 1:
        raise ValueError(
            "top_k must be at least 1."
        )

    query_embedding = generate_embedding(
        normalized_query
    )

    db = SessionLocal()

    try:
        distance = (
            DestinationDocument.embedding.cosine_distance(
                query_embedding
            )
        )

        rows = (
            db.query(
                DestinationDocument,
                distance.label("distance"),
            )
            .filter(
                DestinationDocument.destination
                == normalized_destination
            )
            .order_by(distance)
            .limit(top_k)
            .all()
        )

        results: list[RetrievedChunk] = []

        for document, document_distance in rows:
            similarity = 1.0 - float(
                document_distance
            )

            results.append(
                RetrievedChunk(
                    destination=document.destination,
                    title=document.title,
                    content=document.content,
                    source=document.source,
                    chunk_index=document.chunk_index,
                    similarity=similarity,
                )
            )

        return results

    finally:
        db.close()