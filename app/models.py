from dataclasses import dataclass
from datetime import date, time
from typing import Literal


BookingStatus = Literal["active", "cancelled"]


@dataclass
class BookingRecord:
    id: int
    name: str
    phone: str
    booking_date: date
    booking_time: time
    guests: int
    status: BookingStatus = "active"
