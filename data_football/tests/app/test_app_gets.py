from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from data_football.models import (
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


def test_get_teams_with_result(
    client: TestClient,
    team_url: str,
    team: Team,
):
    # Arrange
    team_base: dict = TeamModel.model_validate(team).model_dump()

    # Act
    response: Response = client.get(team_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"teams": [team_base]}


def test_get_teams_with_no_results(client: TestClient, team_url: str):
    # Act
    response: Response = client.get(team_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"teams": []}


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
