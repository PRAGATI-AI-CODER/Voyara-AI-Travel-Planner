from database.models import Trip

from services.destination_intelligence import (
    build_destination_knowledge_context,
)
from services.destination_service import build_destination_context


def build_itinerary_prompt(trip: Trip) -> str:
    duration_days = (trip.end_date - trip.start_date).days + 1

    destination_context = build_destination_context(trip)
    destination_knowledge = build_destination_knowledge_context(
        trip.destination
    )

    return f"""
You are Voyara, an intelligent AI travel planner.

Generate ONLY the day-by-day itinerary for this trip.

TRIP DETAILS

Destination: {trip.destination}
Start Date: {trip.start_date}
End Date: {trip.end_date}
Duration: {duration_days} days
Travelers: {trip.travelers}
Budget: {trip.budget}
Travel Style: {trip.travel_style}
Interests: {trip.interests}

{destination_context}

{destination_knowledge}

PLANNING REQUIREMENTS

1. Generate exactly {duration_days} itinerary days.
2. Create one entry for every date from {trip.start_date} through {trip.end_date}.
3. Respect the traveler's interests.
4. Respect the requested travel style.
5. Consider the number of travelers.
6. Keep activities appropriate for the stated budget.
7. Provide morning, afternoon, and evening plans for every day.
8. Make the first day appropriate for arrival and settling in.
9. Make the final day appropriate for departure or a relaxed final experience.
10. Avoid repeating the exact same activities on different days.
11. Group geographically close activities when possible.
12. Keep the pace realistic and enjoyable.
13. Prefer destination-specific experiences over generic activities.
14. Balance major attractions with local cultural and food experiences.
15. Avoid unnecessary backtracking between distant areas.
16. Do not invent real-time information such as current opening hours,
    live prices, temporary events, or availability.
17. Treat destination knowledge as planning context, not verified
    real-time information.

IMPORTANT

Return ONLY the itinerary list required by the AIItinerary schema.

Do NOT generate:

- trip_id
- message
- metadata
- planning_type
- budget values
- traveler counts
- start or end dates outside the itinerary entries
- Markdown
- Explanations
- Travel tips
- Commentary
- Code fences
- Additional fields

The Voyara backend will add all trip metadata separately.
""".strip()