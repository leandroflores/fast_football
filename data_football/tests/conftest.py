from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from data_football.app import app

USER_MOCK: dict[str, str] = {
    "id": 1,
    "name": "joao",
    "email": "joao@mail.com",
    "password": "123",
}


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def user_db() -> dict:
    return deepcopy(USER_MOCK)


@pytest.fixture
def user_base() -> dict:
    _user_base: dict = deepcopy(USER_MOCK)
    del _user_base["id"]
    return _user_base


@pytest.fixture
def user_public() -> dict:
    _user_public: dict = deepcopy(USER_MOCK)
    del _user_public["password"]
    return _user_public


@pytest.fixture
def user_delete_message(user_db: dict) -> dict:
    return {"message": f"User [id {user_db["id"]}] deleted"}
