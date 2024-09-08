from copy import deepcopy
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from football.adapters.database import get_session
from football.adapters.models import (
    Championship,
    Match,
    # Player,
    Round,
    Stadium,
    Team,
    User,
    table_registry,
)
from football.app import app
from football.utils import random_int, random_str


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user_url() -> str:
    return "/users/"


@pytest.fixture
def user_mock() -> dict:
    return {
        "id": 1,
        "name": random_str(),
        "email": random_str() + "@mail.com",
        "password": random_str(),
    }


@pytest.fixture
def user(session: Session, user_base: dict) -> User:
    user: User = User(**user_base)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def user_model(user_mock: dict) -> dict:
    return deepcopy(user_mock)


@pytest.fixture
def user_base(user_mock: dict) -> dict:
    _base: dict = deepcopy(user_mock)
    del _base["id"]
    return _base


@pytest.fixture
def user_public(user_mock: dict) -> dict:
    _user_public: dict = deepcopy(user_mock)
    del _user_public["password"]
    return _user_public


@pytest.fixture
def user_delete_message() -> dict:
    return {"message": "User deleted"}


@pytest.fixture
def stadium_url() -> str:
    return "/stadiums/"


@pytest.fixture
def stadium_mock() -> dict:
    return {
        "id": 1,
        "name": random_str(),
        "capacity": random_int(),
        "city": random_str(),
        "country": random_str(),
    }


@pytest.fixture
def stadium(session: Session, stadium_base: dict) -> Stadium:
    stadium: Stadium = Stadium(**stadium_base)
    session.add(stadium)
    session.commit()
    session.refresh(stadium)
    return stadium


@pytest.fixture
def stadium_base(stadium_mock: dict) -> dict:
    base_: dict = deepcopy(stadium_mock)
    del base_["id"]
    return base_


@pytest.fixture
def stadium_model(stadium_mock: dict) -> dict:
    return deepcopy(stadium_mock)


@pytest.fixture
def stadium_delete_message() -> dict:
    return {"message": "Stadium deleted"}


@pytest.fixture
def championship_url() -> str:
    return "/championships/"


@pytest.fixture
def championship_mock() -> dict:
    return {
        "id": 1,
        "name": random_str(),
        "format": random_str(),
        "context": random_str(),
        "country": random_str(),
        "start_year": random_int(1990, 2024),
        "end_year": random_int(1990, 2024),
    }


@pytest.fixture
def championship(session: Session, championship_base: dict) -> Championship:
    championship: Championship = Championship(**championship_base)
    session.add(championship)
    session.commit()
    session.refresh(championship)
    return championship


@pytest.fixture
def championship_base(championship_mock: dict) -> dict:
    base_: dict = deepcopy(championship_mock)
    del base_["id"]
    return base_


@pytest.fixture
def championship_model(championship_mock: dict) -> dict:
    return deepcopy(championship_mock)


@pytest.fixture
def championship_delete_message() -> dict:
    return {"message": "Championship deleted"}


@pytest.fixture
def team_url() -> str:
    return "/teams/"


@pytest.fixture
def team_mock() -> dict:
    return {
        "id": 1,
        "name": random_str(),
        "full_name": random_str(),
        "code": random_str(size=3),
        "country": random_str(),
    }


@pytest.fixture
def team(session: Session, team_base: dict) -> Team:
    team: Team = Team(**team_base)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@pytest.fixture
def team_base(team_mock: dict) -> dict:
    base_: dict = deepcopy(team_mock)
    del base_["id"]
    return base_


@pytest.fixture
def team_model(team_mock: dict) -> dict:
    return deepcopy(team_mock)


@pytest.fixture
def team_delete_message() -> dict:
    return {"message": "Team deleted"}


@pytest.fixture
def round_url() -> str:
    return "/rounds/"


@pytest.fixture
def round_mock(championship_model: dict) -> dict:
    return {
        "id": 1,
        "phase": random_str(),
        "details": random_str(),
        "championship_id": championship_model["id"],
    }


@pytest.fixture
def round(session: Session, round_base: dict) -> Round:
    round: Round = Round(**round_base)
    session.add(round)
    session.commit()
    session.refresh(round)
    return round


@pytest.fixture
def round_base(round_mock: dict) -> dict:
    base_: dict = deepcopy(round_mock)
    del base_["id"]
    return base_


@pytest.fixture
def round_model(round_mock: dict) -> dict:
    return deepcopy(round_mock)


@pytest.fixture
def round_delete_message() -> dict:
    return {"message": "Round deleted"}


@pytest.fixture
def match_url() -> str:
    return "/matches/"


@pytest.fixture
def away_team_mock() -> dict:
    return {
        "id": 2,
        "name": random_str(),
        "full_name": random_str(),
        "code": random_str(3),
        "country": random_str(),
    }


@pytest.fixture
def away_team_base(away_team_mock: dict) -> dict:
    base_: dict = deepcopy(away_team_mock)
    del base_["id"]
    return base_


@pytest.fixture
def away_team_model(away_team_mock: dict) -> dict:
    return deepcopy(away_team_mock)


@pytest.fixture
def away_team(session: Session, away_team_base: dict) -> Team:
    team: Team = Team(**away_team_base)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@pytest.fixture
def match_mock(
    stadium_model: dict,
    round_model: dict,
    team_model: dict,
    away_team_model: dict,
) -> dict:
    return {
        "id": 1,
        "date": datetime.now(),
        "goals_home": random_int(0, 3),
        "goals_away": random_int(0, 3),
        "extra_time": False,
        "goals_extra_time_home": 0,
        "goals_extra_time_away": 0,
        "penalty": False,
        "goals_penalty_home": 0,
        "goals_penalty_away": 0,
        "stadium_id": stadium_model["id"],
        "round_id": round_model["id"],
        "home_team_id": team_model["id"],
        "away_team_id": away_team_model["id"],
    }


@pytest.fixture
def match(session: Session, match_base: dict) -> Match:
    match: Match = Match(**match_base)
    session.add(match)
    session.commit()
    session.refresh(match)
    return match


@pytest.fixture
def match_base(match_mock: dict) -> dict:
    base_: dict = deepcopy(match_mock)
    del base_["id"]
    return base_


@pytest.fixture
def match_model(match_mock: dict) -> dict:
    return deepcopy(match_mock)


@pytest.fixture
def match_delete_message() -> dict:
    return {"message": "Match deleted"}


# @pytest.fixture
# def player_url() -> str:
#     return "/players/"


# @pytest.fixture
# def player_mock(team_mock: dict) -> dict:
#     return {
#         "id": 1,
#         "name": random_str(),
#         "full_name": random_str(),
#         "birth_date": datetime.now(),
#         "current_team_id": team_mock["id"],
#     }


# @pytest.fixture
# def player(session: Session, player_base: dict) -> Player:
#     player: Player = Player(**player_base)
#     session.add(player)
#     session.commit()
#     session.refresh(player)
#     return player


# @pytest.fixture
# def player_base(player_mock: dict) -> dict:
#     base_: dict = deepcopy(player_mock)
#     del base_["id"]
#     return base_


# @pytest.fixture
# def player_model(player_mock: dict) -> dict:
#     return deepcopy(player_mock)


# @pytest.fixture
# def player_delete_message() -> dict:
#     return {"message": "Player deleted"}
