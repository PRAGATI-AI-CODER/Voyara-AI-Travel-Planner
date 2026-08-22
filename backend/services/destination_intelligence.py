from dataclasses import dataclass


@dataclass(frozen=True)
class DestinationKnowledge:
    """
    Represents destination-level knowledge that can be supplied
    to Voyara's planning pipeline.

    This abstraction is intentionally independent from Trip and
    Gemini so that future providers such as travel APIs, RAG,
    or real-time data sources can plug into it.
    """

    destination: str
    overview: str
    planning_notes: list[str]


def get_destination_knowledge(
    destination: str,
) -> DestinationKnowledge:
    """
    Return destination knowledge for the requested destination.

    This is currently a lightweight foundation. It deliberately
    avoids pretending that static data is real-time or verified.
    Future versions can replace this implementation with
    source-backed destination retrieval.
    """

    normalized_destination = destination.strip()

    if not normalized_destination:
        raise ValueError(
            "Destination cannot be empty."
        )

    return DestinationKnowledge(
        destination=normalized_destination,
        overview=(
            f"Plan a trip around the major attractions, "
            f"neighborhoods, local culture, food, and practical "
            f"travel experience of {normalized_destination}."
        ),
        planning_notes=[
            "Prefer destination-specific experiences.",
            "Group geographically close activities when possible.",
            "Balance major attractions with local experiences.",
            "Respect the traveler's interests and travel style.",
            "Do not treat static knowledge as real-time availability.",
        ],
    )


def build_destination_knowledge_context(
    destination: str,
) -> str:
    """
    Convert destination knowledge into prompt-ready context.
    """

    knowledge = get_destination_knowledge(destination)

    notes = "\n".join(
        f"- {note}"
        for note in knowledge.planning_notes
    )

    return f"""
DESTINATION KNOWLEDGE

Destination:
{knowledge.destination}

Overview:
{knowledge.overview}

Planning Notes:
{notes}
""".strip()