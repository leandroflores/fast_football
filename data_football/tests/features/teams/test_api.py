from copy import deepcopy
from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from football.adapters.models import Team
from football.domain.entities import TeamModel
from football.utils import random_str


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


def test_create_team_with_empty_data(
    client: TestClient,
    team_url: str,
):
    # Act
    response: Response = client.post(
        team_url,
        json={},
    )

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_team_with_repeated_name(
    client: TestClient,
    team_url: str,
    team_base: dict,
    team: Team,
):
    # Arrange
    name: str = team_base["name"]
    code: str = random_str(size=3)
    repeated_team: dict = deepcopy(team_base)
    repeated_team["code"] = code

    # Act
    response: Response = client.post(
        team_url,
        json=repeated_team,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "detail": f"Team with name '{name}' already exists"
    }


def test_create_team_with_repeated_code(
    client: TestClient,
    team_url: str,
    team_base: dict,
    team: Team,
):
    # Arrange
    name: str = random_str()
    code: str = team_base["code"]
    repeated_team: dict = deepcopy(team_base)
    repeated_team["name"] = name

    # Act
    response: Response = client.post(
        team_url,
        json=repeated_team,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "detail": f"Team with code '{code}' already exists"
    }


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


def test_get_not_found_team(
    client: TestClient,
    team_url: str,
    team: Team,
):
    # Arrange
    team_id: int = -1

    # Act
    response: Response = client.get(f"{team_url}{team_id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Team not found"}


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


def test_update_with_not_found_team(
    client: TestClient,
    team_url: str,
    team_base: dict,
    team: Team,
):
    # Arrange
    id_team: int = -1
    team_modified: dict = deepcopy(team_base)
    team_modified["name"] = random_str()
    team_modified["code"] = random_str()

    # Act
    response: Response = client.put(
        f"{team_url}{id_team}",
        json=team_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Team not found"}


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


def test_delete_with_not_found_team(
    client: TestClient,
    team_url: str,
    team: Team,
):
    # Arrange
    team_id: int = -1

    # Act
    response: Response = client.delete(f"{team_url}{team_id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Team not found"}
