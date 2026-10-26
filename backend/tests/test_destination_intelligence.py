import sys
from pathlib import Path
from unittest.mock import Mock, patch

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
    build_destination_knowledge_context,
    get_destination_knowledge,
)
from services.providers.geoapify_provider import (
    GeoapifyDestinationKnowledgeProvider,
)


def test_base_provider_returns_knowledge():
    provider = BaseDestinationKnowledgeProvider()

    knowledge = provider.get_knowledge("Paris")

    assert isinstance(knowledge, DestinationKnowledge)
    assert knowledge.destination == "Paris"
    assert knowledge.overview
    assert knowledge.planning_notes


def test_provider_contract():
    assert issubclass(
        BaseDestinationKnowledgeProvider,
        DestinationKnowledgeProvider,
    )

    assert issubclass(
        StaticDestinationKnowledgeProvider,
        DestinationKnowledgeProvider,
    )

    assert issubclass(
        GeoapifyDestinationKnowledgeProvider,
        DestinationKnowledgeProvider,
    )


def test_empty_destination_rejected():
    provider = BaseDestinationKnowledgeProvider()

    try:
        provider.get_knowledge("")
    except ValueError as error:
        assert "Destination cannot be empty" in str(error)
    else:
        raise AssertionError(
            "Expected empty destination to raise ValueError."
        )


def test_resolver_default_static():
    with patch.dict(
        "os.environ",
        {},
        clear=True,
    ):
        resolver = DestinationKnowledgeResolver()
        provider = resolver.resolve()

    assert isinstance(
        provider,
        StaticDestinationKnowledgeProvider,
    )


def test_resolver_custom_provider():
    custom_provider = BaseDestinationKnowledgeProvider()

    resolver = DestinationKnowledgeResolver(
        provider=custom_provider,
    )

    assert resolver.resolve() is custom_provider


def test_get_destination_knowledge_uses_custom_provider():
    custom_provider = BaseDestinationKnowledgeProvider()

    knowledge = get_destination_knowledge(
        "Paris",
        provider=custom_provider,
    )

    assert knowledge.destination == "Paris"
    assert knowledge.overview
    assert knowledge.planning_notes


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

    with patch.dict(
        "os.environ",
        {
            "DESTINATION_PROVIDER": "static",
        },
    ):
        prompt = build_itinerary_prompt(trip)

    assert "DESTINATION KNOWLEDGE" in prompt
    assert "Eiffel Tower" in prompt
    assert "Montmartre" in prompt
    assert "French pastries" in prompt
    assert "Art and museum visits" in prompt


def test_geoapify_provider_requires_api_key():
    with patch.dict(
        "os.environ",
        {},
        clear=True,
    ):
        try:
            GeoapifyDestinationKnowledgeProvider()
        except ValueError as error:
            assert "GEOAPIFY_API_KEY" in str(error)
        else:
            raise AssertionError(
                "Expected missing Geoapify API key to raise ValueError."
            )


def test_geoapify_provider_maps_api_results():
    provider = GeoapifyDestinationKnowledgeProvider(
        api_key="test-key",
    )

    geocode_response = Mock()
    geocode_response.json.return_value = {
        "results": [
            {
                "city": "Paris",
                "place_id": "test-place-id",
            }
        ]
    }
    geocode_response.raise_for_status.return_value = None

    attractions_response = Mock()
    attractions_response.json.return_value = {
        "features": [
            {
                "properties": {
                    "name": "Test Attraction",
                    "categories": [
                        "tourism",
                        "tourism.attraction",
                    ],
                }
            },
            {
                "properties": {
                    "name": "Test Museum",
                    "categories": [
                        "entertainment",
                        "entertainment.museum",
                    ],
                }
            },
        ]
    }
    attractions_response.raise_for_status.return_value = None

    food_response = Mock()
    food_response.json.return_value = {
        "features": [
            {
                "properties": {
                    "name": "Test Cafe",
                    "categories": [
                        "catering",
                        "catering.cafe",
                    ],
                }
            },
            {
                "properties": {
                    "name": "Test Restaurant",
                    "categories": [
                        "catering",
                        "catering.restaurant",
                    ],
                }
            },
        ]
    }
    food_response.raise_for_status.return_value = None

    with patch("requests.Session.get") as mock_get:
        mock_get.side_effect = [
            geocode_response,
            attractions_response,
            food_response,
        ]

        knowledge = provider.get_knowledge("Paris")

    assert knowledge.destination == "Paris"

    assert "Test Attraction" in knowledge.attractions
    assert "Test Museum" in knowledge.attractions

    assert "Test Cafe" in knowledge.food_experiences
    assert "Test Restaurant" in knowledge.food_experiences


def test_geoapify_provider_rejects_empty_destination():
    provider = GeoapifyDestinationKnowledgeProvider(
        api_key="test-key",
    )

    try:
        provider.get_knowledge("")
    except ValueError as error:
        assert "Destination cannot be empty" in str(error)
    else:
        raise AssertionError(
            "Expected empty destination to raise ValueError."
        )


def test_resolver_uses_static_provider_by_default():
    with patch.dict(
        "os.environ",
        {},
        clear=True,
    ):
        resolver = DestinationKnowledgeResolver()
        provider = resolver.resolve()

    assert isinstance(
        provider,
        StaticDestinationKnowledgeProvider,
    )


def test_resolver_selects_geoapify_provider():
    with patch.dict(
        "os.environ",
        {
            "DESTINATION_PROVIDER": "geoapify",
            "GEOAPIFY_API_KEY": "test-key",
        },
        clear=True,
    ):
        resolver = DestinationKnowledgeResolver()
        provider = resolver.resolve()

    assert isinstance(
        provider,
        GeoapifyDestinationKnowledgeProvider,
    )


def test_resolver_falls_back_when_geoapify_key_is_missing():
    with patch.dict(
        "os.environ",
        {
            "DESTINATION_PROVIDER": "geoapify",
        },
        clear=True,
    ):
        resolver = DestinationKnowledgeResolver()
        provider = resolver.resolve()

    assert isinstance(
        provider,
        StaticDestinationKnowledgeProvider,
    )


def test_geoapify_runtime_failure_falls_back_to_static():
    class FailingProvider(DestinationKnowledgeProvider):
        def get_knowledge(
            self,
            destination: str,
        ) -> DestinationKnowledge:
            raise RuntimeError(
                "Simulated Geoapify failure"
            )

    knowledge = get_destination_knowledge(
        "Paris",
        provider=FailingProvider(),
    )

    assert knowledge.destination == "Paris"
    assert "Eiffel Tower" in knowledge.attractions
    assert "Montmartre" in knowledge.neighborhoods
