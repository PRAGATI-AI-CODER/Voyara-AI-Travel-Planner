from sqlalchemy.orm import Session

from database.models import Trip


def create_trip(db: Session, trip_data) -> Trip:
    new_trip = Trip(
        destination=trip_data.destination,
        start_date=trip_data.start_date,
        end_date=trip_data.end_date,
        travelers=trip_data.travelers,
        budget=trip_data.budget,
        travel_style=", ".join(trip_data.travel_style),
        interests=", ".join(trip_data.interests),
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return new_trip


def get_all_trips(db: Session) -> list[Trip]:
    return db.query(Trip).order_by(Trip.id.desc()).all()


def get_trip_by_id(db: Session, trip_id: int) -> Trip | None:
    return db.query(Trip).filter(Trip.id == trip_id).first()


def delete_trip(db: Session, trip: Trip) -> None:
    db.delete(trip)
    db.commit()