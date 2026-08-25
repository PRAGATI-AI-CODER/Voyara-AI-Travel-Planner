from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class DestinationKnowledge:
    """
    Normalized destination knowledge used by Voyara's
    planning pipeline.
    """

    destination: str
    overview: str
    planning_notes: list[str]


class DestinationKnowledgeProvider(ABC):
    """
    Interface for destination knowledge providers.

    Future implementations can retrieve information from
    external APIs, databases, RAG systems, or other sources.
    """

    @abstractmethod
    def get_knowledge(
        self,
        destination: str,
    ) -> DestinationKnowledge:
        """
        Retrieve normalized knowledge for a destination.
        """
        raise NotImplementedError


class BaseDestinationKnowledgeProvider(
    DestinationKnowledgeProvider
):
    """
    Current fallback provider.

    This provider supplies generic planning guidance while
    Voyara's external knowledge integrations are being built.
    """

    def get_knowledge(
        self,
        destination: str,
    ) -> DestinationKnowledge:
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


def get_destination_knowledge(
    destination: str,
    provider: DestinationKnowledgeProvider | None = None,
) -> DestinationKnowledge:
    """
    Retrieve destination knowledge through the configured provider.
    """

    active_provider = (
        provider
        if provider is not None
        else BaseDestinationKnowledgeProvider()
    )

    return active_provider.get_knowledge(destination)


def build_destination_knowledge_context(
    destination: str,
    provider: DestinationKnowledgeProvider | None = None,
) -> str:
    """
    Convert normalized destination knowledge into
    prompt-ready context.
    """

    knowledge = get_destination_knowledge(
        destination,
        provider,
    )

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