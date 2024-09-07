from copy import deepcopy
from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from data_football.models import Stadium, User
from data_football.schemas import StadiumModel, UserPublic
from data_football.utils import random_int, random_str


def test_home(client: TestClient):
    # Act
    response: Response = client.get("/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Data Football Service!"}


# def test_create_user(
#     client: TestClient,
#     user_url: str,
#     user_base: dict,
#     user_public: dict,
# ):
#     # Act
#     response: Response = client.post(
#         user_url,
#         json=user_base,
#     )

#     # Assert
#     assert response.status_code == HTTPStatus.CREATED
#     assert response.json() == user_public


# def test_create_stadium(
#     client: TestClient,
#     stadium_url: str,
#     stadium_base: dict,
#     stadium_model: dict,
# ):
#     # Act
#     response: Response = client.post(
#         stadium_url,
#         json=stadium_base,
#     )

#     # Assert
#     assert response.status_code == HTTPStatus.CREATED
#     assert response.json() == stadium_model


def test_get_users_with_no_results(client: TestClient, user_url: str):
    # Act
    response: Response = client.get(user_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_get_stadiums_with_no_results(client: TestClient, stadium_url: str):
    # Act
    response: Response = client.get(stadium_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"stadiums": []}


def test_get_users_with_users(
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


def test_get_stadiums_with_users(
    client: TestClient,
    stadium_url: str,
    stadium: Stadium,
):
    # Arrange
    stadium_base: dict = StadiumModel.model_validate(stadium).model_dump()

    # Act
    response: Response = client.get(stadium_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"stadiums": [stadium_base]}


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


def test_get_stadium(
    client: TestClient,
    stadium_url: str,
    stadium: Stadium,
):
    # Arrange
    stadium_id: int = 1
    stadium_model: dict = StadiumModel.model_validate(stadium).model_dump()

    # Act
    response: Response = client.get(f"{stadium_url}{stadium_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == stadium_model


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


def test_update_stadium(
    client: TestClient,
    stadium_url: str,
    stadium_base: dict,
    stadium: Stadium,
):
    # Arrange
    id_stadium: int = 1
    stadium_modified: dict = deepcopy(stadium_base)
    stadium_modified["name"] = random_str()
    stadium_modified["capacity"] = random_int()
    stadium_result: dict = deepcopy(stadium_modified)
    stadium_result["id"] = id_stadium

    # Act
    response: Response = client.put(
        f"{stadium_url}{id_stadium}",
        json=stadium_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == stadium_result


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


def test_delete_stadium(
    client: TestClient,
    stadium_url: str,
    stadium_delete_message: str,
    stadium: Stadium,
):
    # Arrange
    stadium_id: int = 1

    # Act
    response: Response = client.delete(f"{stadium_url}{stadium_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == stadium_delete_message
