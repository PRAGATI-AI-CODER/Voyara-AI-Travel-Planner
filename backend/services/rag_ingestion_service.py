from pathlib import Path

from database.database import SessionLocal
from database.rag_models import DestinationDocument
from services.embedding_service import generate_embedding
from services.rag_chunker import chunk_markdown_file


def ingest_destination_document(
    file_path: str | Path,
    destination: str,
) -> int:
    """
    Ingest a destination Markdown document into PostgreSQL.

    The document is:
    1. Split into structured chunks.
    2. Embedded using Gemini.
    3. Stored in destination_documents.

    Returns the number of inserted chunks.
    """

    chunks = chunk_markdown_file(
        file_path=file_path,
        destination=destination,
    )

    if not chunks:
        raise ValueError(
            f"No chunks were generated from: {file_path}"
        )

    db = SessionLocal()

    try:
        existing_count = (
            db.query(DestinationDocument)
            .filter(
                DestinationDocument.destination
                == destination,
                DestinationDocument.source
                == str(file_path),
            )
            .count()
        )

        if existing_count:
            raise ValueError(
                f"Document already ingested: {file_path}"
            )

        documents: list[DestinationDocument] = []

        for chunk in chunks:
            embedding = generate_embedding(
                chunk.content
            )

            documents.append(
                DestinationDocument(
                    destination=chunk.destination,
                    title=chunk.title,
                    content=chunk.content,
                    source=chunk.source,
                    chunk_index=chunk.chunk_index,
                    embedding=embedding,
                )
            )

        db.add_all(documents)
        db.commit()

        return len(documents)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()