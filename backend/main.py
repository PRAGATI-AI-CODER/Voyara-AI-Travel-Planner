from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database.database import Base, engine, get_db
from database.models import Trip
from schemas.trip import (
    TripCreateResponse,
    TripListResponse,
    TripRequest,
    TripResponse,
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
        "trip": new_trip,
    }


@app.get("/api/trips", response_model=TripListResponse)
def get_trips(
    db: Session = Depends(get_db),
):
    trips = db.query(Trip).order_by(Trip.id.desc()).all()

    return {
        "count": len(trips),
        "trips": trips,
    }


@app.get("/api/trips/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: int,
    db: Session = Depends(get_db),
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if trip is None:
        raise HTTPException(
            status_code=404,
            detail="Trip not found",
        )

    return trip


@app.delete("/api/trips/{trip_id}")
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if trip is None:
        raise HTTPException(
            status_code=404,
            detail="Trip not found",
        )

    db.delete(trip)
    db.commit()

    return {
        "message": "Trip deleted successfully",
        "trip_id": trip_id,
    }