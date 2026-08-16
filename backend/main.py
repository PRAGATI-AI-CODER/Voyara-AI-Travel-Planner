from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database.database import Base, engine, get_db
from schemas.trip import (
    ItineraryResponse,
    TripCreateResponse,
    TripListResponse,
    TripRequest,
    TripResponse,
)
from services.ai_planning_service import (
    generate_ai_itinerary,
    generate_best_itinerary,
)
from services.planning_service import generate_itinerary
from services.trip_service import (
    create_trip,
    delete_trip,
    get_all_trips,
    get_trip_by_id,
)


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Voyara API",
    description="AI-powered travel intelligence and itinerary planning API.",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Voyara API is running",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.post("/api/trips", response_model=TripCreateResponse)
def create_trip_endpoint(
    trip: TripRequest,
    db: Session = Depends(get_db),
):
    new_trip = create_trip(db, trip)

    return {
        "message": "Trip created successfully",
        "trip": new_trip,
    }


@app.get("/api/trips", response_model=TripListResponse)
def get_trips(
    db: Session = Depends(get_db),
):
    trips = get_all_trips(db)

    return {
        "count": len(trips),
        "trips": trips,
    }


@app.get("/api/trips/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: int,
    db: Session = Depends(get_db),
):
    trip = get_trip_by_id(db, trip_id)

    if trip is None:
        raise HTTPException(
            status_code=404,
            detail="Trip not found",
        )

    return trip


@app.delete("/api/trips/{trip_id}")
def delete_trip_endpoint(
    trip_id: int,
    db: Session = Depends(get_db),
):
    trip = get_trip_by_id(db, trip_id)

    if trip is None:
        raise HTTPException(
            status_code=404,
            detail="Trip not found",
        )

    delete_trip(db, trip)

    return {
        "message": "Trip deleted successfully",
        "trip_id": trip_id,
    }


@app.get(
    "/api/trips/{trip_id}/itinerary",
    response_model=ItineraryResponse,
)
def get_trip_itinerary(
    trip_id: int,
    db: Session = Depends(get_db),
):
    trip = get_trip_by_id(db, trip_id)

    if trip is None:
        raise HTTPException(
            status_code=404,
            detail="Trip not found",
        )

    itinerary = generate_itinerary(trip)

    duration_days = (trip.end_date - trip.start_date).days + 1

    interests = [
        interest.strip()
        for interest in trip.interests.split(",")
        if interest.strip()
    ]

    return {
        "message": "Itinerary generated successfully",
        "trip_id": trip.id,
        "destination": trip.destination,
        "start_date": trip.start_date,
        "end_date": trip.end_date,
        "metadata": {
            "duration_days": duration_days,
            "travelers": trip.travelers,
            "budget": trip.budget,
            "travel_style": trip.travel_style,
            "interests": interests,
            "planning_type": "deterministic",
        },
        "itinerary": itinerary,
    }


@app.get(
    "/api/trips/{trip_id}/ai-itinerary",
    response_model=ItineraryResponse,
)
def get_ai_trip_itinerary(
    trip_id: int,
    db: Session = Depends(get_db),
):
    trip = get_trip_by_id(db, trip_id)

    if trip is None:
        raise HTTPException(
            status_code=404,
            detail="Trip not found",
        )

    return generate_ai_itinerary(trip)

@app.get(
    "/api/trips/{trip_id}/plan",
    response_model=ItineraryResponse,
)
def get_best_trip_plan(
    trip_id: int,
    db: Session = Depends(get_db),
):
    trip = get_trip_by_id(db, trip_id)

    if trip is None:
        raise HTTPException(
            status_code=404,
            detail="Trip not found",
        )

    return generate_best_itinerary(trip)