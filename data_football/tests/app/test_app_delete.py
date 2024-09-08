from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from data_football.db.models import (
    Championship,
    Round,
    Stadium,
    Team,
    User,
)


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


def test_delete_team(
    client: TestClient,
    team_url: str,
    team_delete_message: str,
    team: Team,
):
    # Arrange
    team_id: int = 1

    # Act
    response: Response = client.delete(f"{team_url}{team_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == team_delete_message


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
