from fastapi import FastAPI

app = FastAPI(
    title="Voyara API",
    description="AI-powered travel intelligence and itinerary planning platform.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Voyara API",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Voyara API",
    }