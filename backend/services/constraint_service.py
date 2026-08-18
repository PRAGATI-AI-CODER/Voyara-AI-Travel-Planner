from datetime import timedelta

from database.models import Trip
from schemas.trip import AIItinerary


TRAVEL_STYLE_RULES = {
    "relaxed": [
        "Keep the daily pace slow and comfortable.",
        "Avoid packing too many major attractions into one day.",
        "Include meaningful free time between major activities.",
        "Prefer leisurely walks, cafes, gardens, cultural experiences, and relaxed meals.",
    ],
    "adventure": [
        "Prioritize active and outdoor experiences.",
        "Include hiking, exploration, nature, or adventure activities when appropriate.",
        "Avoid making every day purely sightseeing or museum-based.",
    ],
    "luxury": [
        "Prioritize premium experiences where the budget genuinely supports them.",
        "Prefer comfort and high-quality experiences.",
        "Do not exceed the stated budget simply because the travel style is luxury.",
    ],
    "budget": [
        "Prioritize affordable and free attractions.",
        "Prefer public transportation and walkable routes.",
        "Avoid unnecessary premium experiences.",
        "Favor local restaurants and reasonably priced food experiences.",
    ],
    "cultural": [
        "Prioritize museums, historical landmarks, heritage sites, local traditions, and cultural experiences.",
        "Include opportunities to understand the destination's history and local culture.",
    ],
    "food": [
        "Prioritize local cuisine, markets, food streets, bakeries, restaurants, and culinary experiences.",
        "Include a variety of food experiences without making every activity food-related.",
    ],
}


INTEREST_RULES = {
    "food": [
        "Include authentic local cuisine and regional specialties.",
        "Include local markets, bakeries, food streets, restaurants, or culinary experiences.",
        "Balance food experiences across different days rather than repeating the same type of meal.",
    ],
    "culture": [
        "Prioritize museums, heritage sites, historical landmarks, and cultural neighborhoods.",
        "Include opportunities to experience local traditions and understand the destination's history.",
        "Balance major cultural attractions with authentic local experiences.",
    ],
    "history": [
        "Prioritize historical landmarks, monuments, heritage sites, and historically significant neighborhoods.",
        "Include context about the destination's historical development through the selected activities.",
    ],
    "nature": [
        "Include parks, gardens, natural scenery, scenic walks, or outdoor experiences.",
        "Balance urban sightseeing with opportunities to experience the destination's natural environment.",
    ],
    "adventure": [
        "Include active outdoor or adventure-oriented experiences where appropriate.",
        "Avoid making the itinerary entirely passive sightseeing.",
    ],
    "shopping": [
        "Include appropriate local markets, shopping districts, artisan stores, or specialty shops.",
        "Prioritize locally distinctive products and souvenirs.",
    ],
    "art": [
        "Prioritize museums, galleries, public art, architecture, and artistic neighborhoods.",
        "Include a mixture of major institutions and local artistic experiences.",
    ],
    "nightlife": [
        "Include appropriate evening entertainment and local nightlife experiences.",
        "Keep nightlife recommendations consistent with the traveler's style and budget.",
    ],
    "beaches": [
        "Prioritize beaches, coastal areas, swimming, seaside walks, or other appropriate coastal activities.",
    ],
}


def validate_trip_constraints(trip: Trip) -> None:
    """
    Validate the fundamental constraints of a saved trip
    before sending it to the AI planner.
    """

    if not trip.destination or not trip.destination.strip():
        raise ValueError("Trip destination cannot be empty.")

    if trip.start_date > trip.end_date:
        raise ValueError("Trip start date cannot be after end date.")

    if trip.travelers < 1:
        raise ValueError("Trip must have at least one traveler.")

    if trip.budget <= 0:
        raise ValueError("Trip budget must be greater than zero.")


def get_trip_duration(trip: Trip) -> int:
    """
    Return the inclusive number of days in the trip.
    """

    return (trip.end_date - trip.start_date).days + 1


def get_daily_budget(trip: Trip) -> float:
    """
    Calculate the approximate total budget available per trip day.
    """

    duration_days = get_trip_duration(trip)

    return trip.budget / duration_days


def get_daily_budget_per_traveler(trip: Trip) -> float:
    """
    Calculate the approximate budget available per traveler per day.
    """

    duration_days = get_trip_duration(trip)

    return trip.budget / trip.travelers / duration_days


def get_travel_style_rules(trip: Trip) -> list[str]:
    """
    Translate the selected travel style into explicit
    planning instructions for the AI.
    """

    styles = [
        style.strip().lower()
        for style in trip.travel_style.split(",")
        if style.strip()
    ]

    rules = []

    for style in styles:
        style_rules = TRAVEL_STYLE_RULES.get(style)

        if style_rules:
            rules.extend(style_rules)

    return rules


def get_interest_rules(trip: Trip) -> list[str]:
    """
    Translate traveler interests into explicit
    planning instructions for the AI.
    """

    interests = [
        interest.strip().lower()
        for interest in trip.interests.split(",")
        if interest.strip()
    ]

    rules = []

    for interest in interests:
        interest_rules = INTEREST_RULES.get(interest)

        if interest_rules:
            rules.extend(interest_rules)

    return rules


def build_constraint_instructions(trip: Trip) -> str:
    """
    Build explicit planning constraints for the AI.
    """

    duration_days = get_trip_duration(trip)
    daily_budget = get_daily_budget(trip)
    daily_budget_per_traveler = get_daily_budget_per_traveler(trip)

    interests = [
        interest.strip()
        for interest in trip.interests.split(",")
        if interest.strip()
    ]

    travel_style = trip.travel_style.strip()

    style_rules = get_travel_style_rules(trip)
    interest_rules = get_interest_rules(trip)

    style_rules_text = "\n".join(
        f"- {rule}"
        for rule in style_rules
    )

    if not style_rules_text:
        style_rules_text = (
            "- Use a balanced and comfortable travel pace."
        )

    interest_rules_text = "\n".join(
        f"- {rule}"
        for rule in interest_rules
    )

    if not interest_rules_text:
        interest_rules_text = (
            "- Use the stated interests as general planning guidance."
        )

    return f"""
STRICT VOYARA PLANNING CONSTRAINTS

Destination:
{trip.destination}

Trip duration:
Exactly {duration_days} days.

Dates:
The itinerary must start on {trip.start_date}
and end on {trip.end_date}.

Travelers:
{trip.travelers}

Total trip budget:
{trip.budget:.2f}

Approximate total budget per day:
{daily_budget:.2f}

Approximate budget per traveler per day:
{daily_budget_per_traveler:.2f}

Travel style:
{travel_style or "Not specified"}

Interests:
{", ".join(interests) if interests else "Not specified"}

TRAVEL STYLE BEHAVIOR

{style_rules_text}

INTEREST PRIORITIES

{interest_rules_text}

CONSTRAINT RULES

1. Generate exactly {duration_days} days.
2. Every itinerary date must fall between {trip.start_date} and {trip.end_date}.
3. Day 1 must use {trip.start_date}.
4. The final day must use {trip.end_date}.
5. Do not create additional days.
6. Do not omit any trip day.
7. Follow the travel-style behavior rules above.
8. Follow the interest-priority rules above.
9. Consider the number of travelers when suggesting activities.
10. Use the approximate daily budget as a planning constraint.
11. Keep recommendations appropriate for the stated total budget.
12. Do not automatically assume that a higher budget means luxury travel.
13. Do not recommend expensive private tours, Michelin-starred dining,
    premium transportation, or luxury experiences unless they are
    appropriate for the traveler's stated budget and style.
14. Prefer affordable or moderate-cost experiences when the budget
    does not clearly support luxury experiences.
15. Avoid unrealistic schedules with too many major activities in one day.
16. Prefer geographically sensible activity grouping.
17. Do not invent live prices, current availability, opening hours,
    temporary events, or reservations.
18. Keep the itinerary geographically centered on the stated destination.
19. If the destination is a specific city or town, do not move the traveler
    to a different unrelated city during the trip.
20. Nearby day trips are allowed only when they are geographically
    reasonable and consistent with the destination.
21. Do not create a multi-city itinerary unless the traveler explicitly
    requests multiple destinations.
22. Treat specific businesses and attractions as recommendations unless
    verified by a future real-time data source.
23. The approximate daily budget is a planning guideline, not an exact
    expense calculation.
24. Do not claim that the itinerary fits an exact real-world price
    without verified pricing data.
25. Do not make every activity revolve around the traveler's interests.
26. Maintain variety while giving the requested interests clear priority.
""".strip()


def validate_ai_itinerary(
    itinerary: AIItinerary,
    trip: Trip,
) -> None:
    """
    Validate the AI-generated itinerary against the saved trip.
    """

    expected_days = get_trip_duration(trip)
    days = itinerary.itinerary

    if len(days) != expected_days:
        raise ValueError(
            f"AI generated {len(days)} days, "
            f"but the trip requires {expected_days} days."
        )

    seen_dates = set()
    seen_day_numbers = set()
    seen_content = set()

    for index, day in enumerate(days, start=1):
        expected_date = trip.start_date + timedelta(days=index - 1)

        if day.day in seen_day_numbers:
            raise ValueError(
                f"Duplicate itinerary day number: {day.day}."
            )

        seen_day_numbers.add(day.day)

        if day.date in seen_dates:
            raise ValueError(
                f"Duplicate itinerary date: {day.date}."
            )

        seen_dates.add(day.date)

        if day.day != index:
            raise ValueError(
                f"Invalid itinerary day number: expected {index}, "
                f"received {day.day}."
            )

        if day.date != expected_date:
            raise ValueError(
                f"Invalid itinerary date for day {index}: "
                f"expected {expected_date}, received {day.date}."
            )

        if day.destination.strip().lower() != trip.destination.strip().lower():
            raise ValueError(
                f"Invalid destination on day {index}: "
                f"expected {trip.destination}, received {day.destination}."
            )

        if not day.morning.strip():
            raise ValueError(
                f"Morning plan is empty for day {index}."
            )

        if not day.afternoon.strip():
            raise ValueError(
                f"Afternoon plan is empty for day {index}."
            )

        if not day.evening.strip():
            raise ValueError(
                f"Evening plan is empty for day {index}."
            )

        content = (
            day.morning.strip().lower(),
            day.afternoon.strip().lower(),
            day.evening.strip().lower(),
        )

        if content in seen_content:
            raise ValueError(
                f"Duplicate daily itinerary content detected on day {index}."
            )

        seen_content.add(content)