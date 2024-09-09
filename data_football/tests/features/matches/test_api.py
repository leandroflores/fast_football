from copy import deepcopy
from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response

from football.adapters.models import (
    Match,
    Round,
    Stadium,
    Team,
)
from football.domain.entities import MatchModel
from football.utils import random_int, random_str


def test_create_match(  # noqa: PLR0913, PLR0917
    client: TestClient,
    match_url: str,
    match_base: dict,
    match_model: dict,
    stadium: Stadium,
    round: Round,
    team: Team,
    away_team: Team,
):
    # Act
    response: Response = client.post(
        match_url,
        json=match_base,
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == match_model


def test_create_match_with_empty_data(
    client: TestClient,
    match_url: str,
):
    # Arrange
    empty: dict = {}

    # Act
    response: Response = client.post(
        match_url,
        json=empty,
    )

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_match_without_stadium(
    client: TestClient,
    match_url: str,
    match_base: dict,
):
    # Arrange
    base: dict = deepcopy(match_base)
    base["stadium_id"] = -1

    # Act
    response: Response = client.post(
        match_url,
        json=base,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Stadium not found"}


def test_create_match_without_round(
    client: TestClient,
    match_url: str,
    match_base: dict,
    stadium: Stadium,
):
    # Arrange
    base: dict = deepcopy(match_base)
    base["round_id"] = -1

    # Act
    response: Response = client.post(
        match_url,
        json=base,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Round not found"}


def test_create_match_without_home_team(
    client: TestClient,
    match_url: str,
    match_base: dict,
    stadium: Stadium,
    round: Round,
):
    # Arrange
    base: dict = deepcopy(match_base)
    base["home_team_id"] = -1

    # Act
    response: Response = client.post(
        match_url,
        json=base,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Home team not found"}


def test_create_match_without_away_team(  # noqa: PLR0913, PLR0917
    client: TestClient,
    match_url: str,
    match_base: dict,
    stadium: Stadium,
    round: Round,
    team: Team,
):
    # Arrange
    base: dict = deepcopy(match_base)
    base["away_team_id"] = -1

    # Act
    response: Response = client.post(
        match_url,
        json=base,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Away team not found"}


def test_create_match_without_same_team(  # noqa: PLR0913, PLR0917
    client: TestClient,
    match_url: str,
    match_base: dict,
    stadium: Stadium,
    round: Round,
    team: Team,
):
    # Arrange
    base: dict = deepcopy(match_base)
    base["away_team_id"] = base["home_team_id"]

    # Act
    response: Response = client.post(
        match_url,
        json=base,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "detail": "Home team can be different from Away team"
    }


def test_create_match_with_repeated_fields(  # noqa: PLR0913, PLR0917
    client: TestClient,
    match_url: str,
    match_base: dict,
    match: Match,
    stadium: Stadium,
    round: Round,
    team: Team,
    away_team: Team,
):
    # Arrange
    base: dict = deepcopy(match_base)

    # Act
    response: Response = client.post(
        match_url,
        json=base,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Match already exists"}


def test_get_match(
    client: TestClient,
    match_url: str,
    match: Match,
):
    # Arrange
    match_id: int = 1
    match_model: dict = MatchModel.model_validate(match).model_dump()

    # Act
    response: Response = client.get(f"{match_url}{match_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == match_model


def test_get_match_with_error(
    client: TestClient,
    match_url: str,
    match: Match,
):
    # Arrange
    match_id: int = -1

    # Act
    response: Response = client.get(f"{match_url}{match_id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Match not found"}


def test_get_matchs_with_result(
    client: TestClient,
    match_url: str,
    match: Match,
):
    # Arrange
    match_base: dict = MatchModel.model_validate(match).model_dump()
    parameters: dict = {
        "round_id": match.round_id,
        "team_id": match.home_team_id,
    }

    # Act
    response: Response = client.get(
        match_url,
        params=parameters,
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"matches": [match_base]}


def test_get_matches_with_no_results(
    client: TestClient,
    match_url: str,
):
    # Arrange
    parameters: dict = {
        "round_id": 0,
        "team_id": 0,
    }

    # Act
    response: Response = client.get(
        match_url,
        params=parameters,
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"matches": []}


def test_update_match(  # noqa: PLR0913, PLR0917
    client: TestClient,
    match_url: str,
    match_base: dict,
    match: Match,
    stadium: Stadium,
    round: Round,
    team: Team,
    away_team: Team,
):
    # Arrange
    id_match: int = 1
    match_modified: dict = deepcopy(match_base)
    match_modified["goals_home"] = random_int(0, 3)
    match_result: dict = deepcopy(match_modified)
    match_result["id"] = id_match

    # Act
    response: Response = client.put(
        f"{match_url}{id_match}",
        json=match_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == match_result


def test_update_match_with_error(
    client: TestClient,
    match_url: str,
    match_base: dict,
    match: Match,
):
    # Arrange
    match_id: int = -1
    match_modified: dict = deepcopy(match_base)
    match_modified["date_hour"] = random_str()

    # Act
    response: Response = client.put(
        f"{match_url}{match_id}",
        json=match_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Match not found"}


def test_update_match_without_stadium(
    client: TestClient,
    match_url: str,
    match_base: dict,
    match: Match,
):
    # Arrange
    match_id: int = 1
    match_modified: dict = deepcopy(match_base)
    match_modified["stadium_id"] = -1

    # Act
    response: Response = client.put(
        f"{match_url}{match_id}",
        json=match_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Stadium not found"}


def test_update_match_without_round(
    client: TestClient,
    match_url: str,
    match_base: dict,
    match: Match,
    stadium: Stadium,
):
    # Arrange
    match_id: int = 1
    match_modified: dict = deepcopy(match_base)
    match_modified["round_id"] = -1

    # Act
    response: Response = client.put(
        f"{match_url}{match_id}",
        json=match_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Round not found"}


def test_update_match_without_home_team(  # noqa: PLR0913, PLR0917
    client: TestClient,
    match_url: str,
    match_base: dict,
    match: Match,
    stadium: Stadium,
    round: Round,
):
    # Arrange
    match_id: int = 1
    match_modified: dict = deepcopy(match_base)
    match_modified["home_team_id"] = -1

    # Act
    response: Response = client.put(
        f"{match_url}{match_id}",
        json=match_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Home team not found"}


def test_update_match_without_away_team(  # noqa: PLR0913, PLR0917
    client: TestClient,
    match_url: str,
    match_base: dict,
    match: Match,
    stadium: Stadium,
    round: Round,
    team: Team,
):
    # Arrange
    match_id: int = 1
    match_modified: dict = deepcopy(match_base)
    match_modified["away_team_id"] = -1

    # Act
    response: Response = client.put(
        f"{match_url}{match_id}",
        json=match_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Away team not found"}


def test_update_match_with_same_team(  # noqa: PLR0913, PLR0917
    client: TestClient,
    match_url: str,
    match_base: dict,
    match: Match,
    stadium: Stadium,
    round: Round,
    team: Team,
    away_team: Team,
):
    # Arrange
    match_id: int = 1
    match_modified: dict = deepcopy(match_base)
    match_modified["away_team_id"] = match.home_team_id

    # Act
    response: Response = client.put(
        f"{match_url}{match_id}",
        json=match_modified,
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "detail": "Home team can be different from Away team"
    }


def test_delete_match(
    client: TestClient,
    match_url: str,
    match_delete_message: str,
    match: Match,
):
    # Arrange
    match_id: int = 1

    # Act
    response: Response = client.delete(f"{match_url}{match_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == match_delete_message


def test_delete_match_with_error(
    client: TestClient,
    match_url: str,
    match_delete_message: str,
    match: Match,
):
    # Arrange
    match_id: int = -1

    # Act
    response: Response = client.delete(f"{match_url}{match_id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Match not found"}
