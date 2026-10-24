from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True)
class DestinationKnowledge:
    """
    Normalized destination knowledge used by Voyara's
    planning pipeline.

    The model is intentionally provider-agnostic so that
    knowledge can later come from static data, APIs,
    databases, RAG systems, or real-time sources.
    """

    destination: str
    overview: str
    planning_notes: list[str]
    attractions: list[str] = field(default_factory=list)
    neighborhoods: list[str] = field(default_factory=list)
    food_experiences: list[str] = field(default_factory=list)
    cultural_experiences: list[str] = field(default_factory=list)


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
    destination-specific knowledge integrations are being built.
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


class StaticDestinationKnowledgeProvider(
    DestinationKnowledgeProvider
):
    """
    Local structured knowledge provider.

    This provider stores a small curated knowledge base locally.
    It is intentionally separated from the fallback provider so
    that it can later be replaced or extended by RAG, APIs,
    databases, or other knowledge sources.
    """

    _knowledge_base = {
        "paris": DestinationKnowledge(
            destination="Paris",
            overview=(
                "Paris is a major cultural and historical destination "
                "known for museums, architecture, neighborhoods, French "
                "cuisine, art, and landmarks along the Seine."
            ),
            planning_notes=[
                "Group attractions by neighborhood to reduce unnecessary travel.",
                "Balance major landmarks with neighborhood exploration.",
                "Include cultural and food experiences when relevant to interests.",
                "Avoid planning too many major attractions in a single day.",
                "Treat this local knowledge as static planning context, not real-time information.",
            ],
            attractions=[
                "Eiffel Tower",
                "Louvre Museum",
                "Notre-Dame area",
                "Arc de Triomphe",
                "Sacré-Cœur and Montmartre",
                "Seine river area",
            ],
            neighborhoods=[
                "Montmartre",
                "Le Marais",
                "Latin Quarter",
                "Saint-Germain-des-Prés",
            ],
            food_experiences=[
                "French pastries",
                "Traditional French cuisine",
                "Local cafés",
                "French cheese and bakery experiences",
            ],
            cultural_experiences=[
                "Art and museum visits",
                "Historic architecture",
                "Neighborhood walks",
                "French cultural experiences",
            ],
        ),
    }

    def get_knowledge(
        self,
        destination: str,
    ) -> DestinationKnowledge:
        normalized_destination = destination.strip()

        if not normalized_destination:
            raise ValueError(
                "Destination cannot be empty."
            )

        knowledge = self._knowledge_base.get(
            normalized_destination.lower()
        )

        if knowledge is not None:
            return knowledge

        return BaseDestinationKnowledgeProvider().get_knowledge(
            normalized_destination
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
        else StaticDestinationKnowledgeProvider()
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

    planning_notes = "\n".join(
        f"- {note}"
        for note in knowledge.planning_notes
    )

    attractions = "\n".join(
        f"- {item}"
        for item in knowledge.attractions
    )

    neighborhoods = "\n".join(
        f"- {item}"
        for item in knowledge.neighborhoods
    )

    food_experiences = "\n".join(
        f"- {item}"
        for item in knowledge.food_experiences
    )

    cultural_experiences = "\n".join(
        f"- {item}"
        for item in knowledge.cultural_experiences
    )

    return f"""
DESTINATION KNOWLEDGE

Destination:
{knowledge.destination}

Overview:
{knowledge.overview}

Planning Notes:
{planning_notes}

Known Attractions:
{attractions if attractions else "- No destination-specific attractions available."}

Known Neighborhoods:
{neighborhoods if neighborhoods else "- No destination-specific neighborhoods available."}

Food Experiences:
{food_experiences if food_experiences else "- No destination-specific food information available."}

Cultural Experiences:
{cultural_experiences if cultural_experiences else "- No destination-specific cultural information available."}
""".strip()