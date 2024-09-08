from copy import deepcopy
from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from football.adapters.models import Stadium
from football.domain.entities import StadiumModel
from football.utils import random_int, random_str


def test_create_stadium(
    client: TestClient,
    stadium_url: str,
    stadium_base: dict,
    stadium_model: dict,
):
    # Act
    response: Response = client.post(
        stadium_url,
        json=stadium_base,
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == stadium_model


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


def test_get_stadiums_with_result(
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


def test_get_stadiums_with_no_results(client: TestClient, stadium_url: str):
    # Act
    response: Response = client.get(stadium_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"stadiums": []}


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
