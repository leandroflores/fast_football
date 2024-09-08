from copy import deepcopy
from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from football.adapters.models import User
from football.domain.entities import UserPublic
from football.utils import random_str


def test_create_user(
    client: TestClient,
    user_url: str,
    user_base: dict,
    user_public: dict,
):
    # Act
    response: Response = client.post(
        user_url,
        json=user_base,
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == user_public


def test_get_user(
    client: TestClient,
    user_url: str,
    user: User,
):
    # Arrange
    user_id: int = 1
    user_public: dict = UserPublic.model_validate(user).model_dump()

    # Act
    response: Response = client.get(f"{user_url}{user_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_public


def test_get_users_with_result(
    client: TestClient,
    user_url: str,
    user: User,
):
    # Arrange
    user_public: dict = UserPublic.model_validate(user).model_dump()

    # Act
    response: Response = client.get(user_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_public]}


def test_get_users_with_no_results(client: TestClient, user_url: str):
    # Act
    response: Response = client.get(user_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_update_user(
    client: TestClient,
    user_url: str,
    user_base: dict,
    user: User,
):
    # Arrange
    id_user: int = 1
    new_name: str = random_str()
    user_modified: dict = deepcopy(user_base)
    user_modified["name"] = new_name
    user_modified["email"] = new_name + "@mail.com"
    user_result: dict = deepcopy(user_modified)
    del user_result["password"]
    user_result["id"] = id_user

    # Act
    response: Response = client.put(
        f"{user_url}{id_user}",
        json=user_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_result


def test_delete_user(
    client: TestClient,
    user_url: str,
    user_delete_message: str,
    user: User,
):
    # Arrange
    user_id: int = 1

    # Act
    response: Response = client.delete(f"{user_url}{user_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_delete_message
