from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.bookings import booking_service


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_store():
    booking_service.reset()
    yield
    booking_service.reset()


def valid_payload(**overrides):
    payload = {
        "name": "Alice",
        "phone": "+71234567890",
        "booking_date": (date.today() + timedelta(days=1)).isoformat(),
        "booking_time": "12:00:00",
        "guests": 2,
    }
    payload.update(overrides)
    return payload


def test_create_and_get_booking():
    response = client.post("/bookings", json=valid_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "active"
    assert data["id"] == 1

    get_response = client.get(f"/bookings/{data['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == data


def test_duplicate_active_slot_returns_409():
    assert client.post("/bookings", json=valid_payload()).status_code == 201

    response = client.post("/bookings", json=valid_payload(name="Bob"))

    assert response.status_code == 409
    assert response.json() == {"detail": "Slot is already booked"}


def test_cancel_frees_slot_and_not_found():
    created = client.post("/bookings", json=valid_payload()).json()

    cancelled = client.delete(f"/bookings/{created['id']}")
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"

    # Отменённая бронь не занимает слот
    assert client.post("/bookings", json=valid_payload(name="Bob")).status_code == 201

    not_found = client.get("/bookings/999")
    assert not_found.status_code == 404
    assert not_found.json() == {"detail": "Booking not found"}


def test_validation_rules():
    assert client.post(
        "/bookings",
        json=valid_payload(phone="89123456789"),
    ).status_code == 422

    assert client.post(
        "/bookings",
        json=valid_payload(booking_time="12:30:00"),
    ).status_code == 422

    assert client.post(
        "/bookings",
        json=valid_payload(guests=11),
    ).status_code == 422