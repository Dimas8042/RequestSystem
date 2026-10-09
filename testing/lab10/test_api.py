import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_create_request_success():
    r = client.post("/requests", json={
        "title": "Тестовая заявка",
        "category_id": 1,
        "author_id": 4
    })
    assert r.status_code == 201
    assert r.json()["Title"] == "Тестовая заявка"


def test_change_status():
    r = client.patch("/requests/1", json={"status_id": 2})
    assert r.status_code == 200
    assert r.json()["StatusId"] == 2


def test_list_requests_returns_array():
    r = client.get("/requests")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_get_existing_request():
    r = client.get("/requests/1")
    assert r.status_code == 200
    assert r.json()["Id"] == 1


def test_get_missing_request_404():
    r = client.get("/requests/9999")
    assert r.status_code == 404
    assert r.json()["error"] == "not_found"


def test_delete_request():
    r_create = client.post("/requests", json={
        "title": "Для удаления",
        "category_id": 1,
        "author_id": 4
    })
    new_id = r_create.json()["Id"]
    r_del = client.delete(f"/requests/{new_id}")
    assert r_del.status_code == 204
    r_get = client.get(f"/requests/{new_id}")
    assert r_get.status_code == 404


def test_short_title_422():
    r = client.post("/requests", json={
        "title": "ab",
        "category_id": 1,
        "author_id": 4
    })
    assert r.status_code == 422


def test_empty_title_422():
    r = client.post("/requests", json={
        "title": "",
        "category_id": 1,
        "author_id": 4
    })
    assert r.status_code == 422


def test_regression_category_must_exist():
    r = client.post("/requests", json={
        "title": "Тест категории",
        "category_id": 999,
        "author_id": 4
    })
    assert r.status_code == 400


def test_regression_assignee_must_exist():
    r = client.patch("/requests/1", json={"assignee_id": 999})
    assert r.status_code == 400


def test_users_list():
    r = client.get("/users")
    assert r.status_code == 200
    assert len(r.json()) >= 4


def test_statuses_list():
    r = client.get("/statuses")
    assert r.status_code == 200


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"