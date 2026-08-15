from database.models import Trip
from schemas.trip import AIItinerary, ItineraryResponse
from services.ai_service import generate_structured_ai_response
from services.prompt_service import build_itinerary_prompt


def generate_ai_itinerary(trip: Trip) -> ItineraryResponse:
    prompt = build_itinerary_prompt(trip)

    ai_result = generate_structured_ai_response(
        prompt,
        AIItinerary,
    )

    duration_days = (trip.end_date - trip.start_date).days + 1

    interests = [
        interest.strip()
        for interest in trip.interests.split(",")
        if interest.strip()
    ]

    return ItineraryResponse(
        message="Itinerary generated successfully",
        trip_id=trip.id,
        destination=trip.destination,
        start_date=trip.start_date,
        end_date=trip.end_date,
        metadata={
            "duration_days": duration_days,
            "travelers": trip.travelers,
            "budget": trip.budget,
            "travel_style": trip.travel_style,
            "interests": interests,
            "planning_type": "ai",
        },
        itinerary=ai_result.itinerary,
    )