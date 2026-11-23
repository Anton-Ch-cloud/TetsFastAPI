from datetime import date
from threading import Lock

from app.exceptions import BookingNotFound, SlotAlreadyBooked
from app.models import BookingRecord
from app.schemas import BookingCreate


class BookingService:
    def __init__(self) -> None:
        self._bookings: dict[int, BookingRecord] = {}
        self._next_id = 1
        self._lock = Lock()

    def reset(self) -> None:
        with self._lock:
            self._bookings.clear()
            self._next_id = 1

    def create(self, data: BookingCreate) -> BookingRecord:
        with self._lock:
            for record in self._bookings.values():
                if (
                    record.status == "active"
                    and record.booking_date == data.booking_date
                    and record.booking_time == data.booking_time
                ):
                    raise SlotAlreadyBooked()

            record = BookingRecord(
                id=self._next_id,
                name=data.name,
                phone=data.phone,
                booking_date=data.booking_date,
                booking_time=data.booking_time,
                guests=data.guests,
            )
            self._bookings[record.id] = record
            self._next_id += 1
            return record

    def list(self, booking_date: date | None = None) -> list[BookingRecord]:
        with self._lock:
            records = list(self._bookings.values())

        if booking_date is not None:
            records = [record for record in records if record.booking_date == booking_date]

        return sorted(records, key=lambda record: record.id)

    def get(self, booking_id: int) -> BookingRecord:
        with self._lock:
            record = self._bookings.get(booking_id)

        if record is None:
            raise BookingNotFound()

        return record

    def cancel(self, booking_id: int) -> BookingRecord:
        with self._lock:
            record = self._bookings.get(booking_id)
            if record is None:
                raise BookingNotFound()

            record.status = "cancelled"
            return record


booking_service = BookingService()
