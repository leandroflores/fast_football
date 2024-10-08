from copy import deepcopy
from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from football.adapters.models import Championship, Round
from football.domain.entities import RoundModel
from football.utils import random_str


def test_create_round(
    client: TestClient,
    round_url: str,
    round_base: dict,
    round_model: dict,
    championship: Championship,
):
    # Act
    response: Response = client.post(
        round_url,
        json=round_base,
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == round_model


def test_create_round_with_empty_data(
    client: TestClient,
    round_url: str,
):
    # Act
    response: Response = client.post(
        round_url,
        json={},
    )

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_round_with_invalid_championship(
    client: TestClient,
    round_url: str,
    round_base: dict,
):
    # Act
    response: Response = client.post(
        round_url,
        json=round_base,
    )

    # Assert
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Integrity error to process request"}


def test_get_round(
    client: TestClient,
    round_url: str,
    round: Round,
):
    # Arrange
    round_id: int = 1
    round_model: dict = RoundModel.model_validate(round).model_dump()

    # Act
    response: Response = client.get(f"{round_url}{round_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == round_model


def test_get_round_not_found(
    client: TestClient,
    round_url: str,
    round: Round,
):
    # Arrange
    round_id: int = -1

    # Act
    response: Response = client.get(f"{round_url}{round_id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Round not found"}


def test_get_rounds_with_result(
    client: TestClient,
    round_url: str,
    round: Round,
):
    # Arrange
    round_base: dict = RoundModel.model_validate(round).model_dump()

    # Act
    response: Response = client.get(round_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"rounds": [round_base]}


def test_get_rounds_with_no_results(client: TestClient, round_url: str):
    # Act
    response: Response = client.get(round_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"rounds": []}


def test_update_round(
    client: TestClient,
    round_url: str,
    round_base: dict,
    round: Round,
    championship: Championship,
):
    # Arrange
    id_round: int = 1
    round_modified: dict = deepcopy(round_base)
    round_modified["phase"] = random_str()
    round_modified["details"] = random_str()
    round_result: dict = deepcopy(round_modified)
    round_result["id"] = id_round

    # Act
    response: Response = client.put(
        f"{round_url}{id_round}",
        json=round_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == round_result


def test_update_with_not_found_round(
    client: TestClient,
    round_url: str,
    round: Round,
):
    # Arrange
    round_id: int = -1

    # Act
    response: Response = client.get(f"{round_url}{round_id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Round not found"}


def test_update_round_with_not_found_championship(
    client: TestClient,
    round_url: str,
    round_base: dict,
    round: Round,
):
    id_round: int = 1
    round_modified: dict = deepcopy(round_base)
    round_modified["phase"] = random_str()
    round_modified["details"] = random_str()
    round_modified["championship_id"] = -5

    # Act
    response: Response = client.put(
        f"{round_url}{id_round}",
        json=round_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Championship not found"}


def test_delete_round(
    client: TestClient,
    round_url: str,
    round_delete_message: str,
    round: Round,
):
    # Arrange
    round_id: int = 1

    # Act
    response: Response = client.delete(f"{round_url}{round_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == round_delete_message


def test_delete_round_not_found(
    client: TestClient,
    round_url: str,
    round: Round,
):
    # Arrange
    round_id: int = -1

    # Act
    response: Response = client.delete(f"{round_url}{round_id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Round not found"}
