from copy import deepcopy
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
from data_football.utils import random_int, random_str


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


def test_update_team(
    client: TestClient,
    team_url: str,
    team_base: dict,
    team: Team,
):
    # Arrange
    id_team: int = 1
    team_modified: dict = deepcopy(team_base)
    team_modified["name"] = random_str()
    team_modified["code"] = random_str()
    team_result: dict = deepcopy(team_modified)
    team_result["id"] = id_team

    # Act
    response: Response = client.put(
        f"{team_url}{id_team}",
        json=team_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == team_result


def test_update_round(
    client: TestClient,
    round_url: str,
    round_base: dict,
    round: Round,
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
