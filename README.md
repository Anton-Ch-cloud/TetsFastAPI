# Restaurant Booking API

Небольшое REST API для бронирования столика: создание брони, список броней,
получение по id и отмена.

## Стек

- Python 3.11+
- FastAPI
- Pydantic v2
- In-memory storage
- Pytest

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload