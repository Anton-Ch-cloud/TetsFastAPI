from datetime import date

from fastapi import APIRouter, Query, status

from app.schemas import BookingCreate, BookingOut
from app.services.bookings import booking_service


router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate) -> BookingOut:
    record = booking_service.create(payload)
    return BookingOut.model_validate(record)


@router.get("", response_model=list[BookingOut])
def list_bookings(
    booking_date: date | None = Query(default=None, alias="date"),
) -> list[BookingOut]:
    records = booking_service.list(booking_date)
    return [BookingOut.model_validate(record) for record in records]


@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int) -> BookingOut:
    record = booking_service.get(booking_id)
    return BookingOut.model_validate(record)


@router.delete("/{booking_id}", response_model=BookingOut)
def cancel_booking(booking_id: int) -> BookingOut:
    record = booking_service.cancel(booking_id)
    return BookingOut.model_validate(record)

