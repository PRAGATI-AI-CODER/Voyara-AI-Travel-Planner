from database.models import Trip


def build_destination_context(trip: Trip) -> str:
    """
    Build a structured destination context from the user's trip.

    This is the foundation of Voyara's Destination Intelligence layer.
    It prepares destination and traveler information for downstream
    AI planning and future real-world travel data integrations.
    """

    interests = [
        interest.strip()
        for interest in trip.interests.split(",")
        if interest.strip()
    ]

    return f"""
DESTINATION INTELLIGENCE CONTEXT

Destination:
{trip.destination}

Travel dates:
{trip.start_date} to {trip.end_date}

Duration:
{(trip.end_date - trip.start_date).days + 1} days

Travelers:
{trip.travelers}

Budget:
{trip.budget}

Travel style:
{trip.travel_style}

Interests:
{", ".join(interests) if interests else "None specified"}

PLANNING REQUIREMENTS:
- Keep recommendations relevant to the destination.
- Respect the requested travel style.
- Prioritize the user's stated interests.
- Keep activities practical for the available duration.
- Avoid unnecessarily long-distance movements.
- Maintain geographic consistency within the itinerary.
""".strip()