from database.models import Trip
from schemas.trip import AIItinerary, ItineraryResponse
from services.ai_service import generate_structured_ai_response
from services.constraint_service import (
    build_constraint_instructions,
    validate_ai_itinerary,
    validate_trip_constraints,
)
from services.prompt_service import build_itinerary_prompt


MAX_ITINERARY_ATTEMPTS = 2


def generate_ai_itinerary(trip: Trip) -> ItineraryResponse:
    validate_trip_constraints(trip)

    base_prompt = build_itinerary_prompt(trip)
    constraint_prompt = build_constraint_instructions(trip)

    prompt = f"""
{base_prompt}

{constraint_prompt}
""".strip()

    last_error = None

    for attempt in range(1, MAX_ITINERARY_ATTEMPTS + 1):
        try:
            ai_result = generate_structured_ai_response(
                prompt,
                AIItinerary,
            )

            validate_ai_itinerary(
                ai_result,
                trip,
            )

            duration_days = (
                trip.end_date - trip.start_date
            ).days + 1

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

        except ValueError as error:
            last_error = error

            if attempt == MAX_ITINERARY_ATTEMPTS:
                break

            prompt = f"""
{prompt}

CORRECTION REQUIRED

The previous generated itinerary failed Voyara's validation.

Validation error:
{error}

Generate a completely corrected itinerary.

You MUST:
- Generate exactly the required number of days.
- Use the correct dates.
- Use the correct destination.
- Include morning, afternoon, and evening plans.
- Follow every constraint in the original prompt.
- Return only the structured itinerary.
""".strip()

    raise ValueError(
        "AI itinerary failed validation after "
        f"{MAX_ITINERARY_ATTEMPTS} attempts: {last_error}"
    )