from sqlalchemy import select
from sqlalchemy.orm import Session

from football.adapters import models


def test_create_user(user_model: dict, session: Session):
    # Arrange
    new_user: models.User = models.User(
        name=user_model["name"],
        email=user_model["email"],
        password=user_model["password"],
    )

    # Act
    session.add(new_user)
    session.commit()

    # Assert
    user: models.User = session.scalar(
        select(models.User).where(models.User.name == user_model["name"])
    )

    assert user.name == user_model["name"]
    assert user.email == user_model["email"]
    assert user.password == user_model["password"]


def test_create_stadium(stadium_model: dict, session: Session):
    # Arrange
    new_stadium: models.Stadium = models.Stadium(
        name=stadium_model["name"],
        capacity=stadium_model["capacity"],
        city=stadium_model["city"],
        country=stadium_model["country"],
    )

    # Act
    session.add(new_stadium)
    session.commit()

    # Assert
    stadium: models.Stadium = session.scalar(
        select(models.Stadium).where(
            models.Stadium.name == stadium_model["name"]
        )
    )

    assert stadium.name == stadium_model["name"]
    assert stadium.capacity == stadium_model["capacity"]
    assert stadium.city == stadium_model["city"]
    assert stadium.country == stadium_model["country"]


def test_create_championship(championship_model: dict, session: Session):
    # Arrange
    new_championship: models.Championship = models.Championship(
        name=championship_model["name"],
        format=championship_model["format"],
        context=championship_model["context"],
        country=championship_model["country"],
        start_year=championship_model["start_year"],
        end_year=championship_model["end_year"],
    )

    # Act
    session.add(new_championship)
    session.commit()

    # Assert
    championship: models.Championship = session.scalar(
        select(models.Championship).where(
            models.Championship.name == championship_model["name"]
        )
    )

    assert championship.name == championship_model["name"]
    assert championship.format == championship_model["format"]
    assert championship.context == championship_model["context"]
    assert championship.country == championship_model["country"]
    assert championship.start_year == championship_model["start_year"]
    assert championship.end_year == championship_model["end_year"]


def test_create_team(team_model: dict, session: Session):
    # Arrange
    new_team: models.Team = models.Team(
        name=team_model["name"],
        full_name=team_model["full_name"],
        code=team_model["code"],
        country=team_model["country"],
    )

    # Act
    session.add(new_team)
    session.commit()

    # Assert
    team: models.Team = session.scalar(
        select(models.Team).where(
            (models.Team.name == team_model["name"])
            & (models.Team.code == team_model["code"])
        )
    )

    assert team.name == team_model["name"]
    assert team.full_name == team_model["full_name"]
    assert team.code == team_model["code"]
    assert team.country == team_model["country"]


def test_create_round(round_model: dict, session: Session):
    # Arrange
    new_round: models.Round = models.Round(
        phase=round_model["phase"],
        details=round_model["details"],
        championship_id=round_model["championship_id"],
    )

    # Act
    session.add(new_round)
    session.commit()

    # Assert
    round: models.Round = session.scalar(
        select(models.Round).where(
            (models.Round.phase == round_model["phase"])
            & (models.Round.details == round_model["details"])
            & (models.Round.championship_id == round_model["championship_id"])
        )
    )

    assert round.phase == round_model["phase"]
    assert round.details == round_model["details"]
    assert round.championship_id == round_model["championship_id"]
