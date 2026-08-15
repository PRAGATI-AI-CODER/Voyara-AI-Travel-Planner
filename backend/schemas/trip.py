from datetime import date

from pydantic import BaseModel, Field, field_validator


class TripRequest(BaseModel):
    destination: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Travel destination",
    )

    start_date: date = Field(
        ...,
        description="Trip start date",
    )

    end_date: date = Field(
        ...,
        description="Trip end date",
    )

    travelers: int = Field(
        ...,
        ge=1,
        le=50,
        description="Number of travelers",
    )

    budget: float = Field(
        ...,
        gt=0,
        description="Approximate trip budget",
    )

    travel_style: list[str] = Field(
        default_factory=list,
        description="Preferred travel styles",
    )

    interests: list[str] = Field(
        default_factory=list,
        description="Traveler interests",
    )

    @field_validator("destination")
    @classmethod
    def validate_destination(cls, value: str) -> str:
        return value.strip()

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, value: date, info):
        start_date = info.data.get("start_date")

        if start_date and value < start_date:
            raise ValueError("End date cannot be before start date.")

        return value


class TripResponse(BaseModel):
    id: int
    destination: str
    start_date: date
    end_date: date
    travelers: int
    budget: float
    travel_style: str
    interests: str


class TripListResponse(BaseModel):
    count: int
    trips: list[TripResponse]


class TripCreateResponse(BaseModel):
    message: str
    trip: TripResponse


class ItineraryDay(BaseModel):
    day: int
    date: date
    destination: str
    morning: str
    afternoon: str
    evening: str


class ItineraryMetadata(BaseModel):
    duration_days: int
    travelers: int
    budget: float
    travel_style: str
    interests: list[str]
    planning_type: str


class ItineraryResponse(BaseModel):
    message: str
    trip_id: int
    destination: str
    start_date: date
    end_date: date
    metadata: ItineraryMetadata
    itinerary: list[ItineraryDay]