from pydantic import BaseModel, Field


class RequestCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str | None = None
    category_id: int
    author_id: int


class RequestUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=255)
    description: str | None = None
    category_id: int | None = None
    status_id: int | None = None
    assignee_id: int | None = None


class RequestOut(BaseModel):
    id: int
    title: str
    description: str | None
    status_id: int
    category_id: int
    author_id: int
    assignee_id: int | None
    created_at: str