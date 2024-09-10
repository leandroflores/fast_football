from copy import deepcopy
from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from football.adapters.models import Player, Team
from football.domain.entities import PlayerModel
from football.utils import random_str

random_str()


def test_create_player(
    client: TestClient,
    player_url: str,
    player_base: dict,
    player_model: dict,
    team: Team,
):
    # Act
    response: Response = client.post(
        player_url,
        json=player_base,
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == player_model


def test_create_player_with_empty_data(
    client: TestClient,
    player_url: str,
):
    # Act
    response: Response = client.post(
        player_url,
        json={},
    )

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_round_without_team(
    client: TestClient,
    player_url: str,
    player_base: dict,
):
    # Arrange
    base: dict = deepcopy(player_base)
    base["current_team_id"] = -1

    # Act
    response: Response = client.post(
        player_url,
        json=base,
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Current Team not found"}


def test_get_player(
    client: TestClient,
    player_url: str,
    player: Player,
):
    # Arrange
    player_id: int = 1
    player_model: dict = PlayerModel.model_validate(player).model_dump()

    # Act
    response: Response = client.get(f"{player_url}{player_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == player_model


def test_get_not_found_player(
    client: TestClient,
    player_url: str,
    player: Player,
):
    # Arrange
    player_id: int = -1

    # Act
    response: Response = client.get(f"{player_url}{player_id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Player not found"}


def test_get_players_by_team(
    client: TestClient,
    player_url: str,
    player_model: PlayerModel,
    player: Player,
    team: Team,
):
    # Arrange
    team_id: int = team.id

    # Act
    response: Response = client.get(f"{player_url}team/{team_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"players": [player_model]}


def test_get_players_with_invalid_team(
    client: TestClient,
    player_url: str,
    player: Player,
    team: Team,
):
    # Arrange
    team_id: int = -1

    # Act
    response: Response = client.get(f"{player_url}team/{team_id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Team not found"}


def test_get_players_with_result(
    client: TestClient,
    player_url: str,
    player: Player,
):
    # Arrange
    player_base: dict = PlayerModel.model_validate(player).model_dump()

    # Act
    response: Response = client.get(player_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"players": [player_base]}


def test_get_players_with_no_results(
    client: TestClient,
    player_url: str,
):
    # Act
    response: Response = client.get(player_url)

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"players": []}


def test_update_player(
    client: TestClient,
    player_url: str,
    player_base: dict,
    player: Player,
    team: Team,
):
    # Arrange
    id_player: int = 1
    player_modified: dict = deepcopy(player_base)
    player_modified["name"] = random_str()
    player_modified["full_name"] = random_str()
    player_result: dict = deepcopy(player_modified)
    player_result["id"] = id_player

    # Act
    response: Response = client.put(
        f"{player_url}{id_player}",
        json=player_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == player_result


def test_update_not_found_player(
    client: TestClient,
    player_url: str,
    player_base: dict,
    player: Player,
):
    # Arrange
    player_id: int = -1

    # Act
    response: Response = client.put(
        f"{player_url}{player_id}",
        json=player_base,
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Player not found"}


def test_update_player_without_team(
    client: TestClient,
    player_url: str,
    player_base: dict,
    player: Player,
    team: Team,
):
    # Arrange
    player_id: int = player.id
    player_modified: dict = deepcopy(player_base)
    player_modified["name"] = random_str()
    player_modified["current_team_id"] = -1

    # Act
    response: Response = client.put(
        f"{player_url}{player_id}",
        json=player_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Current team not found"}


def test_delete_player(
    client: TestClient,
    player_url: str,
    player_delete_message: str,
    player: Player,
):
    # Arrange
    player_id: int = 1

    # Act
    response: Response = client.delete(f"{player_url}{player_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == player_delete_message


def test_delete_player_not_found(
    client: TestClient,
    player_url: str,
    player: Player,
):
    # Arrange
    player_id: int = -1

    # Act
    response: Response = client.delete(f"{player_url}{player_id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Player not found"}
