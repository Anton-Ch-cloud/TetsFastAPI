from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import BookingNotFound, SlotAlreadyBooked
from app.routes.bookings import router as bookings_router


app = FastAPI(
    title="Restaurant Booking API",
    version="1.0.0",
)

app.include_router(bookings_router)


@app.exception_handler(BookingNotFound)
async def booking_not_found_handler(
    request: Request,
    exc: BookingNotFound,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": "Booking not found"},
    )


@app.exception_handler(SlotAlreadyBooked)
async def slot_already_booked_handler(
    request: Request,
    exc: SlotAlreadyBooked,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": "Slot is already booked"},
    )
