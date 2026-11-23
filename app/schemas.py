from datetime import date, time, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookingCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    phone: str = Field(pattern=r"^\+7\d{10}$")
    booking_date: date
    booking_time: time
    guests: int = Field(ge=1, le=10)

    @field_validator("booking_date")
    @classmethod
    def validate_booking_date(cls, value: date) -> date:
        today = date.today()
        if value < today:
            raise ValueError("booking_date must not be in the past")
        if value > today + timedelta(days=30):
            raise ValueError("booking_date must be within 30 days from today")
        return value

    @field_validator("booking_time")
    @classmethod
    def validate_booking_time(cls, value: time) -> time:
        if value.tzinfo is not None:
            raise ValueError("booking_time must not contain timezone")
        if value.minute != 0 or value.second != 0 or value.microsecond != 0:
            raise ValueError("booking_time must be a whole hour")
        if not (12 <= value.hour <= 22):
            raise ValueError("booking_time must be between 12:00 and 22:00")
        return value


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    booking_date: date
    booking_time: time
    guests: int
    status: Literal["active", "cancelled"]
