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
        new_id = self.repo.create(data.model_dump())
        return self.get_request(new_id)

    def update_request(self, request_id: int, data: RequestUpdate):
        self.get_request(request_id)
        self.repo.update(request_id, data.model_dump(exclude_none=True))
        return self.get_request(request_id)

    def delete_request(self, request_id: int):
        self.get_request(request_id)
        return self.repo.delete(request_id)