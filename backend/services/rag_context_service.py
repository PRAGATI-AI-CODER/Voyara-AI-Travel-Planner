from services.rag_retriever import retrieve_destination_chunks


DEFAULT_RAG_TOP_K = 3


def build_rag_context(
    destination: str,
    query: str,
    top_k: int = DEFAULT_RAG_TOP_K,
) -> str:
    """
    Retrieve relevant destination knowledge and format it
    for inclusion in the itinerary planning prompt.
    """

    chunks = retrieve_destination_chunks(
        destination=destination,
        query=query,
        top_k=top_k,
    )

    if not chunks:
        return (
            "RAG DESTINATION KNOWLEDGE\n\n"
            "No relevant destination knowledge was found."
        )

    sections = [
        "RAG DESTINATION KNOWLEDGE",
        "",
        (
            "The following knowledge was retrieved from "
            "Voyara's destination knowledge base."
        ),
        (
            "Use it as planning context. Do not treat it "
            "as verified real-time information."
        ),
        "",
    ]

    for index, chunk in enumerate(chunks, start=1):
        sections.extend(
            [
                f"[Knowledge {index}]",
                f"Topic: {chunk.title}",
                f"Relevance: {chunk.similarity:.4f}",
                chunk.content,
                "",
            ]
        )

    return "\n".join(sections).strip()