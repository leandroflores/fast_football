from copy import deepcopy
from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from football.adapters.models import Championship
from football.domain.entities import ChampionshipModel
from football.utils import random_str


def test_create_championship(
    client: TestClient,
    championship_url: str,
    championship_base: dict,
    championship_model: dict,
):
    # Act
    response: Response = client.post(
        championship_url,
        json=championship_base,
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == championship_model


def test_create_championship_with_empty_data(
    client: TestClient,
    championship_url: str,
):
    # Arrange
    wrong_championship: dict = {}

    # Act
    response: Response = client.post(
        championship_url,
        json=wrong_championship,
    )

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_championship_with_error(
    client: TestClient,
    championship_url: str,
):
    # Arrange
    incomplete_championship: dict = {"name": random_str()}

    # Act
    response: Response = client.post(
        championship_url,
        json=incomplete_championship,
    )

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_championship(
    client: TestClient,
    championship_url: str,
    championship: Championship,
):
    # Arrange
    championship_id: int = 1
    championship_model: dict = ChampionshipModel.model_validate(
        championship
    ).model_dump()

    # Act
    response: Response = client.get(f"{championship_url}{championship_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == championship_model


def test_get_championships_with_result(
    client: TestClient,
    championship_url: str,
    championship: Championship,
):
    # Arrange
    championship_base: dict = ChampionshipModel.model_validate(
        championship
    ).model_dump()

    # Act
    response: Response = client.get(championship_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"championships": [championship_base]}


def test_get_championships_with_no_results(
    client: TestClient, championship_url: str
):
    # Act
    response: Response = client.get(championship_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"championships": []}


def test_update_championship(
    client: TestClient,
    championship_url: str,
    championship_base: dict,
    championship: Championship,
):
    # Arrange
    id_championship: int = 1
    championship_modified: dict = deepcopy(championship_base)
    championship_modified["name"] = random_str()
    championship_modified["format"] = random_str()
    championship_modified["context"] = random_str()
    championship_result: dict = deepcopy(championship_modified)
    championship_result["id"] = id_championship

    # Act
    response: Response = client.put(
        f"{championship_url}{id_championship}",
        json=championship_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == championship_result


def test_delete_championship(
    client: TestClient,
    championship_url: str,
    championship_delete_message: str,
    championship: Championship,
):
    # Arrange
    championship_id: int = 1

    # Act
    response: Response = client.delete(f"{championship_url}{championship_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == championship_delete_message
