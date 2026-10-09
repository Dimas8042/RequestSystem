from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.db import init_db
from src.models import RequestCreate, RequestUpdate, RequestOut
from src.repository import UserRepository, StatusRepository, CategoryRepository
from src.service import RequestService, NotFoundError, ValidationError

app = FastAPI(title="RequestSystem API", version="1.0.0")

service = RequestService()
users_repo = UserRepository()
statuses_repo = StatusRepository()
categories_repo = CategoryRepository()


@app.on_event("startup")
def on_startup():
    init_db()


@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    return JSONResponse(status_code=422, content={"error": "validation_error", "message": str(exc)})


@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"error": "not_found", "message": str(exc)})


@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc):
    return JSONResponse(status_code=400, content={"error": "bad_request", "message": str(exc)})


@app.get("/health", summary="Проверка работоспособности")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/requests", summary="Список заявок")
def list_requests(status_id: int | None = None, category_id: int | None = None, q: str | None = None):
    return service.list_requests(status_id, category_id, q)


@app.get("/requests/{request_id}", summary="Одна заявка")
def get_request(request_id: int):
    return service.get_request(request_id)


@app.post("/requests", status_code=201, summary="Создание заявки")
def create_request(data: RequestCreate, response: Response):
    created = service.create_request(data)
    response.headers["Location"] = f"/requests/{created['Id']}"
    return created


@app.patch("/requests/{request_id}", summary="Изменение заявки")
def update_request(request_id: int, data: RequestUpdate):
    return service.update_request(request_id, data)


@app.delete("/requests/{request_id}", status_code=204, summary="Удаление заявки")
def delete_request(request_id: int):
    service.delete_request(request_id)
    return Response(status_code=204)


@app.get("/users", summary="Список пользователей")
def list_users():
    return users_repo.list()


@app.get("/statuses", summary="Справочник статусов")
def list_statuses():
    return statuses_repo.list()


@app.get("/categories", summary="Справочник категорий")
def list_categories():
    return categories_repo.list()