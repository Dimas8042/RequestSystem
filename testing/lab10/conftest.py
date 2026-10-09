import os
import pytest


@pytest.fixture(autouse=True, scope="session")
def setup_db():
    """Перед запуском тестов убеждаемся, что БД существует."""
    from src.db import init_db
    init_db()
    yield