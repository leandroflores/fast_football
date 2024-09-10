from copy import deepcopy
from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from football.adapters.models import (
    Goal,
    Match,
    Player,
    Team,
)
from football.domain.entities import GoalModel
from football.utils import random_int


def test_create_goal(  # noqa: PLR0913, PLR0917
    client: TestClient,
    goal_url: str,
    goal_base: dict,
    goal_model: dict,
    match: Match,
    team: Team,
    player: Player,
):
    # Act
    response: Response = client.post(
        goal_url,
        json=goal_base,
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == goal_model


def test_create_goal_with_empty_data(
    client: TestClient,
    goal_url: str,
):
    # Arrange
    empty: dict = {}

    # Act
    response: Response = client.post(
        goal_url,
        json=empty,
    )

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_goal_without_match(
    client: TestClient,
    goal_url: str,
    goal_base: dict,
):
    # Arrange
    base: dict = deepcopy(goal_base)
    base["match_id"] = -1

    # Act
    response: Response = client.post(
        goal_url,
        json=base,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Match not found"}


def test_create_goal_without_team(  # noqa: PLR0913, PLR0917
    client: TestClient,
    goal_url: str,
    goal_base: dict,
    goal_model: dict,
    match: Match,
    player: Player,
    team: Team,
):
    # Arrange
    base: dict = deepcopy(goal_base)
    base["team_id"] = -1

    # Act
    response: Response = client.post(
        goal_url,
        json=base,
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == goal_model


def test_create_goal_without_player(  # noqa: PLR0913, PLR0917
    client: TestClient,
    goal_url: str,
    goal_base: dict,
    goal: Goal,
    match: Match,
    player: Player,
    team: Team,
):
    # Arrange
    base: dict = deepcopy(goal_base)
    base["player_id"] = -1

    # Act
    response: Response = client.post(
        goal_url,
        json=base,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Player not found"}


def test_get_goal(
    client: TestClient,
    goal_url: str,
    goal: Goal,
):
    # Arrange
    goal_id: int = 1
    goal_model: dict = GoalModel.model_validate(goal).model_dump()

    # Act
    response: Response = client.get(f"{goal_url}{goal_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == goal_model


def test_get_not_found_goal(
    client: TestClient,
    goal_url: str,
    goal: Goal,
):
    # Arrange
    goal_id: int = -1

    # Act
    response: Response = client.get(f"{goal_url}{goal_id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Goal not found"}


def test_get_goals_with_result(
    client: TestClient,
    goal_url: str,
    goal: Goal,
):
    # Arrange
    goal_base: dict = GoalModel.model_validate(goal).model_dump()
    parameters: dict = {
        "match_id": goal.match_id,
    }

    # Act
    response: Response = client.get(
        goal_url,
        params=parameters,
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"goals": [goal_base]}


def test_get_goals_with_no_results(
    client: TestClient,
    goal_url: str,
):
    # Arrange
    parameters: dict = {"match_id": 0}

    # Act
    response: Response = client.get(
        goal_url,
        params=parameters,
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"goals": []}


def test_update_goal(  # noqa: PLR0913, PLR0917
    client: TestClient,
    goal_url: str,
    goal_base: dict,
    goal: Goal,
    match: Match,
    player: Player,
    team: Team,
):
    # Arrange
    id_goal: int = 1
    goal_modified: dict = deepcopy(goal_base)
    goal_modified["minute"] = random_int(0, 90)
    goal_result: dict = deepcopy(goal_modified)
    goal_result["id"] = id_goal

    # Act
    response: Response = client.put(
        f"{goal_url}{id_goal}",
        json=goal_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == goal_result


def test_update_goal_with_invalid_id(
    client: TestClient,
    goal_url: str,
    goal_base: dict,
    goal: Goal,
):
    # Arrange
    match_id: int = -1
    match_modified: dict = deepcopy(goal_base)
    match_modified["minute"] = random_int(0, 90)

    # Act
    response: Response = client.put(
        f"{goal_url}{match_id}",
        json=match_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Goal not found"}


def test_update_goal_without_match(
    client: TestClient,
    goal_url: str,
    goal_base: dict,
    goal: Goal,
):
    # Arrange
    goal_id: int = 1
    goal_modified: dict = deepcopy(goal_base)
    goal_modified["match_id"] = -1

    # Act
    response: Response = client.put(
        f"{goal_url}{goal_id}",
        json=goal_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Match not found"}


def test_update_goal_without_player(
    client: TestClient,
    goal_url: str,
    goal_base: dict,
    goal: Goal,
    match: Match,
):
    # Arrange
    goal_id: int = 1
    goal_modified: dict = deepcopy(goal_base)
    goal_modified["player_id"] = -1

    # Act
    response: Response = client.put(
        f"{goal_url}{goal_id}",
        json=goal_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Player not found"}


def test_delete_goal(
    client: TestClient,
    goal_url: str,
    goal_delete_message: str,
    goal: Goal,
):
    # Arrange
    goal_id: int = 1

    # Act
    response: Response = client.delete(f"{goal_url}{goal_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == goal_delete_message


def test_delete_goal_with_error(
    client: TestClient,
    goal_url: str,
    goal_delete_message: str,
    goal: Goal,
):
    # Arrange
    goal_id: int = -1

    # Act
    response: Response = client.delete(f"{goal_url}{goal_id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Goal not found"}
