from copy import deepcopy
from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response


def test_home(client: TestClient):
    # Act
    response: Response = client.get("/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo!"}


def test_create_user(client: TestClient, user_base: dict, user_public: dict):
    # Act
    response: Response = client.post(
        "/users/",
        json=user_base,
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == user_public


def test_get_user(client: TestClient, user_public: dict):
    # Act
    response: Response = client.get("/users/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_public]}


def test_update_user(client: TestClient, user_db: dict):
    # Arrange
    id_user: int = user_db["id"]
    user_modified: dict = deepcopy(user_db)
    del user_modified["id"]
    user_modified["email"] = "mail@test.com"

    user_result: dict = deepcopy(user_db)
    user_result["email"] = "mail@test.com"
    del user_result["password"]

    # Act
    response: Response = client.put(f"/users/{id_user}", json=user_modified)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_result


def test_delete_user(
    client: TestClient, user_db: dict, user_delete_message: str
):
    # Arrange
    user_id: int = user_db["id"]

    # Act
    response: Response = client.delete(f"/users/{user_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_delete_message
