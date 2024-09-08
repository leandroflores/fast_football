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
from data_football.schemas import (
    ChampionshipModel,
    RoundModel,
    StadiumModel,
    TeamModel,
    UserPublic,
)


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


def test_get_team(
    client: TestClient,
    team_url: str,
    team: Team,
):
    # Arrange
    team_id: int = 1
    team_model: dict = TeamModel.model_validate(team).model_dump()

    # Act
    response: Response = client.get(f"{team_url}{team_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == team_model


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
