from services.destination_intelligence import (
    BaseDestinationKnowledgeProvider,
    DestinationKnowledge,
    DestinationKnowledgeProvider,
)


def test_base_provider_returns_destination_knowledge():
    provider = BaseDestinationKnowledgeProvider()

    result = provider.get_knowledge("Paris")

    assert isinstance(result, DestinationKnowledge)
    assert result.destination == "Paris"
    assert result.overview
    assert result.planning_notes


def test_provider_contract_is_defined():
    assert issubclass(
        BaseDestinationKnowledgeProvider,
        DestinationKnowledgeProvider,
    )


def test_empty_destination_is_rejected():
    provider = BaseDestinationKnowledgeProvider()

    try:
        provider.get_knowledge("")
        raise AssertionError(
            "Empty destination should have been rejected."
        )
    except ValueError:
        pass