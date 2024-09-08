from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from data_football.db.models import Championship


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


def test_create_team(
    client: TestClient,
    team_url: str,
    team_base: dict,
    team_model: dict,
):
    # Act
    response: Response = client.post(
        team_url,
        json=team_base,
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == team_model


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
