from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database.database import Base, engine, get_db
from database.models import Trip
from schemas.trip import TripRequest


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


@app.post("/api/trips")
def create_trip(
    trip: TripRequest,
    db: Session = Depends(get_db),
):
    new_trip = Trip(
        destination=trip.destination,
        start_date=trip.start_date,
        end_date=trip.end_date,
        travelers=trip.travelers,
        budget=trip.budget,
        travel_style=", ".join(trip.travel_style),
        interests=", ".join(trip.interests),
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return {
        "message": "Trip created successfully",
        "trip": {
            "id": new_trip.id,
            "destination": new_trip.destination,
            "start_date": new_trip.start_date,
            "end_date": new_trip.end_date,
            "travelers": new_trip.travelers,
            "budget": new_trip.budget,
            "travel_style": new_trip.travel_style,
            "interests": new_trip.interests,
        },
    }


@app.get("/api/trips")
def get_trips(
    db: Session = Depends(get_db),
):
    trips = db.query(Trip).order_by(Trip.id.desc()).all()

    return {
        "count": len(trips),
        "trips": [
            {
                "id": trip.id,
                "destination": trip.destination,
                "start_date": trip.start_date,
                "end_date": trip.end_date,
                "travelers": trip.travelers,
                "budget": trip.budget,
                "travel_style": trip.travel_style,
                "interests": trip.interests,
            }
            for trip in trips
        ],
    }