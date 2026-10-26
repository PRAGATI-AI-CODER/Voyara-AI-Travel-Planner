import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

from services.destination_intelligence import (
    BaseDestinationKnowledgeProvider,
    DestinationKnowledge,
    DestinationKnowledgeProvider,
    DestinationKnowledgeResolver,
    StaticDestinationKnowledgeProvider,
    get_destination_knowledge,
)


def test_base_provider_returns_destination_knowledge():
    provider = BaseDestinationKnowledgeProvider()

    knowledge = provider.get_knowledge("Tokyo")

    assert isinstance(knowledge, DestinationKnowledge)
    assert knowledge.destination == "Tokyo"
    assert knowledge.overview
    assert knowledge.planning_notes


def test_provider_contract_is_defined():
    assert issubclass(
        StaticDestinationKnowledgeProvider,
        DestinationKnowledgeProvider,
    )

    assert issubclass(
        BaseDestinationKnowledgeProvider,
        DestinationKnowledgeProvider,
    )


def test_empty_destination_is_rejected():
    provider = BaseDestinationKnowledgeProvider()

    try:
        provider.get_knowledge("   ")
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == "Destination cannot be empty."


def test_resolver_uses_static_provider_by_default():
    resolver = DestinationKnowledgeResolver()

    provider = resolver.resolve()

    assert isinstance(
        provider,
        StaticDestinationKnowledgeProvider,
    )


def test_resolver_accepts_custom_provider():
    class TestProvider(DestinationKnowledgeProvider):
        def get_knowledge(
            self,
            destination: str,
        ) -> DestinationKnowledge:
            return DestinationKnowledge(
                destination=destination,
                overview="Test destination",
                planning_notes=["Test planning note"],
            )

    custom_provider = TestProvider()
    resolver = DestinationKnowledgeResolver(custom_provider)

    resolved_provider = resolver.resolve()

    assert resolved_provider is custom_provider


def test_get_destination_knowledge_uses_custom_provider():
    class TestProvider(DestinationKnowledgeProvider):
        def get_knowledge(
            self,
            destination: str,
        ) -> DestinationKnowledge:
            return DestinationKnowledge(
                destination=destination,
                overview="Custom provider result",
                planning_notes=["Custom provider note"],
            )

    knowledge = get_destination_knowledge(
        "Test City",
        provider=TestProvider(),
    )

    assert knowledge.destination == "Test City"
    assert knowledge.overview == "Custom provider result"
    assert knowledge.planning_notes == [
        "Custom provider note"
    ]


def test_destination_knowledge_is_included_in_itinerary_prompt():
    from datetime import date
    from database.models import Trip
    from services.prompt_service import build_itinerary_prompt

    trip = Trip(
        id=1,
        destination="Paris",
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 3),
        travelers=2,
        budget=50000,
        travel_style="relaxed",
        interests="Food, Culture",
    )

    prompt = build_itinerary_prompt(trip)

    assert "DESTINATION KNOWLEDGE" in prompt
    assert "Eiffel Tower" in prompt
    assert "Montmartre" in prompt
    assert "French pastries" in prompt
    assert "Art and museum visits" in prompt
