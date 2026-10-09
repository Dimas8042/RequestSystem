from src.repository import RequestRepository
from src.models import RequestCreate, RequestUpdate


class NotFoundError(Exception):
    pass


class ValidationError(Exception):
    pass


class RequestService:
    def __init__(self):
        self.repo = RequestRepository()

    def list_requests(self, status_id=None, category_id=None, q=None):
        return self.repo.list(status_id, category_id, q)

    def get_request(self, request_id: int):
        req = self.repo.get(request_id)
        if not req:
            raise NotFoundError(f"Заявка №{request_id} не найдена")
        return req

    def create_request(self, data: RequestCreate):
        if not data.title.strip():
            raise ValidationError("Тема обязательна")
        if self.repo.get_category(data.category_id) is None:
            raise ValidationError(f"Категория {data.category_id} не существует")
        if self.repo.get_user(data.author_id) is None:
            raise ValidationError(f"Автор {data.author_id} не существует")
        new_id = self.repo.create(data.model_dump())
        return self.get_request(new_id)

    def update_request(self, request_id: int, data: RequestUpdate):
        self.get_request(request_id)
        if data.category_id is not None:
            if self.repo.get_category(data.category_id) is None:
                raise ValidationError(f"Категория {data.category_id} не существует")
        if data.assignee_id is not None:
            if self.repo.get_user(data.assignee_id) is None:
                raise ValidationError(f"Исполнитель {data.assignee_id} не существует")
        if data.status_id is not None:
            if self.repo.get_status(data.status_id) is None:
                raise ValidationError(f"Статус {data.status_id} не существует")
        self.repo.update(request_id, data.model_dump(exclude_none=True))
        return self.get_request(request_id)

    def delete_request(self, request_id: int):
        self.get_request(request_id)
        return self.repo.delete(request_id)