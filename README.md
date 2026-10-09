# RequestSystem

Система учёта заявок. Учебный проект по дисциплине "Технологии разработки программного обеспечения".

## Стек
Python 3.12, FastAPI, SQLite, Docker

## Локальный запуск
1. Установить Python 3.12+
2. pip install -r requirements.txt
3. python -m uvicorn src.api:app --reload
4. Открыть http://localhost:8000/docs

## API
- GET /requests
- GET /requests/{id}
- POST /requests
- PATCH /requests/{id}
- DELETE /requests/{id}
- GET /users
- GET /statuses
- GET /categories
- GET /health

## Docker
docker compose up -d

## Деплой
1. VPS с Ubuntu 22.04
2. apt install docker.io docker-compose
3. git clone ...
4. cp .env.example .env
5. docker compose up -d
6. Открыть http://<ip>:8000/docs