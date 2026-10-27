import sys
from pathlib import Path

import pytest


BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from services.rag_chunker import chunk_markdown_file
from services.rag_context_service import build_rag_context


KNOWLEDGE_FILE = (
    BACKEND_DIR
    / "knowledge"
    / "destinations"
    / "paris_overview.md"
)


def test_paris_document_is_split_into_six_chunks():
    chunks = chunk_markdown_file(
        KNOWLEDGE_FILE,
        "Paris",
    )

    assert len(chunks) == 6

    assert [
        chunk.title
        for chunk in chunks
    ] == [
        "Destination",
        "Major Attractions",
        "Neighborhoods",
        "Food and Local Experiences",
        "Culture",
        "Planning Considerations",
    ]


def test_chunks_have_required_metadata():
    chunks = chunk_markdown_file(
        KNOWLEDGE_FILE,
        "Paris",
    )

    for index, chunk in enumerate(chunks):
        assert chunk.destination == "Paris"
        assert chunk.source == str(KNOWLEDGE_FILE)
        assert chunk.chunk_index == index
        assert chunk.title
        assert chunk.content


def test_rag_context_formats_retrieved_chunks(monkeypatch):
    class FakeChunk:
        title = "Neighborhoods"
        content = (
            "Montmartre is known for its artistic atmosphere."
        )
        similarity = 0.91

    def fake_retrieve(
        destination,
        query,
        top_k,
    ):
        assert destination == "Paris"
        assert "cultural" in query
        assert top_k == 3

        return [FakeChunk()]

    monkeypatch.setattr(
        "services.rag_context_service.retrieve_destination_chunks",
        fake_retrieve,
    )

    context = build_rag_context(
        destination="Paris",
        query="Find cultural experiences in Paris.",
        top_k=3,
    )

    assert "RAG DESTINATION KNOWLEDGE" in context
    assert "Neighborhoods" in context
    assert "Montmartre is known" in context
    assert "0.9100" in context


def test_rag_context_handles_no_results(monkeypatch):
    def fake_retrieve(
        destination,
        query,
        top_k,
    ):
        return []

    monkeypatch.setattr(
        "services.rag_context_service.retrieve_destination_chunks",
        fake_retrieve,
    )

    context = build_rag_context(
        destination="Paris",
        query="Unknown destination topic",
    )

    assert (
        "No relevant destination knowledge was found."
        in context
    )