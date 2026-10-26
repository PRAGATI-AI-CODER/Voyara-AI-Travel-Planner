import os

import requests

from services.destination_intelligence import (
    DestinationKnowledge,
    DestinationKnowledgeProvider,
)


GEOCODING_URL = "https://api.geoapify.com/v1/geocode/search"
PLACES_URL = "https://api.geoapify.com/v2/places"

DEFAULT_LIMIT = 10
DEFAULT_TIMEOUT = 15
MAX_RESULTS_PER_GROUP = 10


class GeoapifyDestinationKnowledgeProvider(
    DestinationKnowledgeProvider
):
    """
    Destination knowledge provider backed by Geoapify.

    The provider:
    1. Resolves a destination to a Geoapify place.
    2. Retrieves tourism and food POIs.
    3. Filters and ranks returned POIs.
    4. Normalizes them into DestinationKnowledge.
    """

    def __init__(
        self,
        api_key: str | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        limit: int = DEFAULT_LIMIT,
    ):
        self.api_key = (
            api_key
            or os.getenv("GEOAPIFY_API_KEY")
        )

        self.timeout = timeout
        self.limit = min(
            max(limit, 1),
            MAX_RESULTS_PER_GROUP,
        )

        if not self.api_key:
            raise ValueError(
                "GEOAPIFY_API_KEY is not configured."
            )

    def _geocode_destination(
        self,
        destination: str,
        session: requests.Session,
    ) -> dict:
        response = session.get(
            GEOCODING_URL,
            params={
                "text": destination,
                "type": "city",
                "limit": 1,
                "format": "json",
                "apiKey": self.api_key,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        if not results:
            raise ValueError(
                f"Geoapify could not resolve destination: "
                f"{destination}"
            )

        return results[0]

    def _search_places(
        self,
        place_id: str,
        categories: str,
        session: requests.Session,
    ) -> list[dict]:
        response = session.get(
            PLACES_URL,
            params={
                "categories": categories,
                "filter": f"place:{place_id}",
                "limit": self.limit,
                "lang": "en",
                "apiKey": self.api_key,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        return [
            feature.get("properties", {})
            for feature in data.get("features", [])
        ]

    @staticmethod
    def _category_score(
        categories: list[str],
    ) -> int:
        """
        Score POIs according to useful tourism categories.

        Higher scores represent more directly relevant
        travel attractions.
        """

        category_set = set(categories)

        score = 0

        if "tourism.attraction" in category_set:
            score += 5

        if "tourism.sights" in category_set:
            score += 4

        if "entertainment.museum" in category_set:
            score += 4

        if "tourism.attraction.viewpoint" in category_set:
            score += 2

        if "tourism.sights.ruines" in category_set:
            score -= 2

        return score

    @classmethod
    def _extract_names(
        cls,
        places: list[dict],
    ) -> list[str]:
        """
        Extract useful, unique POI names.

        Results are ranked using Geoapify category metadata.
        """

        candidates: list[tuple[int, int, str]] = []

        for index, place in enumerate(places):
            name = place.get("name")

            if not isinstance(name, str):
                continue

            normalized_name = name.strip()

            if not normalized_name:
                continue

            categories = place.get("categories", [])

            if not isinstance(categories, list):
                categories = []

            tourism_categories = [
                category
                for category in categories
                if isinstance(category, str)
            ]

            score = cls._category_score(
                tourism_categories
            )

            if score <= 0:
                continue

            candidates.append(
                (
                    score,
                    index,
                    normalized_name,
                )
            )

        candidates.sort(
            key=lambda item: (
                -item[0],
                item[1],
            )
        )

        names: list[str] = []
        seen: set[str] = set()

        for _, _, name in candidates:
            key = name.casefold()

            if key in seen:
                continue

            seen.add(key)
            names.append(name)

            if len(names) >= MAX_RESULTS_PER_GROUP:
                break

        return names

    @staticmethod
    def _extract_food_names(
        places: list[dict],
    ) -> list[str]:
        """
        Extract unique restaurant and cafe names.
        """

        names: list[str] = []
        seen: set[str] = set()

        for place in places:
            name = place.get("name")

            if not isinstance(name, str):
                continue

            normalized_name = name.strip()

            if not normalized_name:
                continue

            categories = place.get("categories", [])

            if not isinstance(categories, list):
                categories = []

            is_food_venue = any(
                isinstance(category, str)
                and (
                    category.startswith(
                        "catering.restaurant"
                    )
                    or category.startswith(
                        "catering.cafe"
                    )
                )
                for category in categories
            )

            if not is_food_venue:
                continue

            key = normalized_name.casefold()

            if key in seen:
                continue

            seen.add(key)
            names.append(normalized_name)

            if len(names) >= MAX_RESULTS_PER_GROUP:
                break

        return names

    def get_knowledge(
        self,
        destination: str,
    ) -> DestinationKnowledge:
        normalized_destination = destination.strip()

        if not normalized_destination:
            raise ValueError(
                "Destination cannot be empty."
            )

        with requests.Session() as session:
            location = self._geocode_destination(
                normalized_destination,
                session,
            )

            place_id = location.get("place_id")

            if not place_id:
                raise ValueError(
                    "Geoapify geocoding result did not "
                    "contain a place_id."
                )

            attractions = self._search_places(
                place_id,
                (
                    "tourism.attraction,"
                    "tourism.sights,"
                    "entertainment.museum"
                ),
                session,
            )

            food = self._search_places(
                place_id,
                (
                    "catering.restaurant,"
                    "catering.cafe"
                ),
                session,
            )

        attraction_names = self._extract_names(
            attractions
        )

        food_names = self._extract_food_names(
            food
        )

        city = (
            location.get("city")
            or location.get("name")
            or normalized_destination
        )

        overview = (
            f"Geoapify destination data for {city}, "
            f"including tourism attractions, cultural "
            f"places, restaurants, and cafes."
        )

        planning_notes = [
            "Use externally retrieved places as destination-specific planning context.",
            "Prefer grouping geographically close activities.",
            "Balance attractions with food and cultural experiences.",
            "Treat place availability and opening hours as potentially time-sensitive.",
            "Do not treat provider data as verified real-time availability.",
        ]

        return DestinationKnowledge(
            destination=city,
            overview=overview,
            planning_notes=planning_notes,
            attractions=attraction_names,
            neighborhoods=[],
            food_experiences=food_names,
            cultural_experiences=[],
        )