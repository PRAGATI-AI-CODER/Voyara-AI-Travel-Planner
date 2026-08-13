from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas.trip import TripRequest

app = FastAPI(
    title="Voyara API",
    description="AI-powered travel intelligence and itinerary planning platform.",
    version="0.2.0",
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
        "message": "Welcome to Voyara API",
        "version": "0.2.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Voyara API",
    }


@app.post("/api/trips")
def create_trip(trip: TripRequest):
    return {
        "message": "Trip received successfully.",
        "trip": trip.model_dump(mode="json"),
    }