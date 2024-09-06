from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from data_football.models import User
from data_football.schemas import UserPublic


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


def test_get_users_with_no_results(client: TestClient):
    # Act
    response: Response = client.get("/users/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_get_users_with_users(client: TestClient, user: User):
    # Arrange
    user_public: dict = UserPublic.model_validate(user).model_dump()

    # Act
    response: Response = client.get("/users/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_public]}


def test_get_user(client: TestClient, user: User):
    # Arrange
    user_id: int = 1
    user_public: dict = UserPublic.model_validate(user).model_dump()

    # Act
    response: Response = client.get(f"/users/{user_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_public


def test_update_user(client: TestClient, user: User):
    # Arrange
    id_user: int = 1

    # Act
    response: Response = client.put(
        f"/users/{id_user}",
        json={
            "name": "pedro",
            "email": "pedro@mail.com",
            "password": "123",
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "name": "pedro",
        "email": "pedro@mail.com",
    }


def test_delete_user(client: TestClient, user: User):
    # Arrange
    user_id: int = 1

    # Act
    response: Response = client.delete(f"/users/{user_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}
