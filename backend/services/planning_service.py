from datetime import timedelta

from database.models import Trip


def generate_itinerary(trip: Trip) -> list[dict]:
    interests = [
        interest.strip().lower()
        for interest in trip.interests.split(",")
        if interest.strip()
    ]

    travel_style = trip.travel_style.strip().lower()

    total_days = (trip.end_date - trip.start_date).days + 1

    itinerary = []

    current_date = trip.start_date
    day_number = 1

    while current_date <= trip.end_date:
        is_first_day = day_number == 1
        is_last_day = day_number == total_days

        morning_activity = get_morning_activity(
            trip.destination,
            interests,
            travel_style,
            day_number,
            total_days,
            is_first_day,
            is_last_day,
        )

        afternoon_activity = get_afternoon_activity(
            trip.destination,
            interests,
            travel_style,
            trip.budget,
            day_number,
            total_days,
            is_first_day,
            is_last_day,
        )

        evening_activity = get_evening_activity(
            trip.destination,
            interests,
            travel_style,
            day_number,
            total_days,
            is_first_day,
            is_last_day,
        )

        itinerary.append(
            {
                "day": day_number,
                "date": current_date,
                "destination": trip.destination,
                "morning": morning_activity,
                "afternoon": afternoon_activity,
                "evening": evening_activity,
            }
        )

        current_date += timedelta(days=1)
        day_number += 1

    return itinerary


def get_morning_activity(
    destination: str,
    interests: list[str],
    travel_style: str,
    day_number: int,
    total_days: int,
    is_first_day: bool,
    is_last_day: bool,
) -> str:
    if is_first_day:
        return (
            f"Arrive in {destination}, settle in, and get oriented with "
            f"the local area."
        )

    if is_last_day:
        return (
            f"Enjoy a relaxed final morning in {destination} and revisit "
            f"a favorite nearby place."
        )

    if "culture" in interests and day_number % 2 == 0:
        return (
            f"Explore cultural landmarks, museums, and heritage sites "
            f"in {destination}."
        )

    if "history" in interests:
        return f"Visit important historical landmarks in {destination}."

    if "nature" in interests:
        return f"Start the day with a nature experience around {destination}."

    if "adventure" in interests:
        return f"Begin the day with an adventurous activity in {destination}."

    if travel_style == "relaxed":
        return (
            f"Enjoy a relaxed morning exploring {destination} "
            f"at your own pace."
        )

    return f"Explore a popular morning attraction in {destination}."


def get_afternoon_activity(
    destination: str,
    interests: list[str],
    travel_style: str,
    budget: float,
    day_number: int,
    total_days: int,
    is_first_day: bool,
    is_last_day: bool,
) -> str:
    if is_first_day:
        return (
            f"Take a gentle introduction to {destination} and discover "
            f"nearby attractions."
        )

    if is_last_day:
        return (
            f"Enjoy some free time for last-minute shopping, souvenirs, "
            f"or a final experience in {destination}."
        )

    if "food" in interests and day_number % 2 == 1:
        return (
            f"Discover local cuisine, traditional dishes, and popular "
            f"food experiences in {destination}."
        )

    if "shopping" in interests:
        return f"Explore local markets and shopping areas in {destination}."

    if "nature" in interests:
        return (
            f"Spend the afternoon exploring scenic places "
            f"around {destination}."
        )

    if "adventure" in interests:
        return (
            f"Enjoy an adventure-focused experience "
            f"in {destination}."
        )

    if budget >= 75000:
        return f"Enjoy a premium travel experience in {destination}."

    return f"Explore another popular attraction in {destination}."


def get_evening_activity(
    destination: str,
    interests: list[str],
    travel_style: str,
    day_number: int,
    total_days: int,
    is_first_day: bool,
    is_last_day: bool,
) -> str:
    if is_first_day:
        return (
            f"Have a relaxed welcome dinner and experience "
            f"the evening atmosphere of {destination}."
        )

    if is_last_day:
        return (
            f"Enjoy a memorable final evening in {destination} "
            f"and reflect on the trip."
        )

    if "food" in interests:
        return (
            f"Enjoy a local dinner and experience the food culture "
            f"of {destination}."
        )

    if "culture" in interests and day_number % 2 == 0:
        return (
            f"Experience the local culture and evening atmosphere "
            f"of {destination}."
        )

    if travel_style == "relaxed":
        return (
            f"Have a relaxed evening and enjoy the atmosphere "
            f"of {destination}."
        )

    return (
        f"Explore the evening attractions and local atmosphere "
        f"of {destination}."
    )