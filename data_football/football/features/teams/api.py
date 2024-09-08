import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from psycopg import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from football.adapters.database import get_session
from football.adapters.models import Team
from football.domain.entities import (
    Message,
    TeamBase,
    TeamList,
    TeamModel,
)
from football.utils import update_object

router: APIRouter = APIRouter()
logger: logging.Logger = logging.getLogger(__name__)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=TeamModel)
def create_team(team: TeamBase, session: Session = Depends(get_session)):
    try:
        record = session.scalar(
            select(Team).where(
                (Team.name == team.name) | (Team.code == team.code)
            )
        )
        if record:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Team '{team.name} [{team.code}]' already exists",
            )

        new_team: Team = Team(**team.model_dump())

        session.add(new_team)
        session.commit()
        session.refresh(new_team)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Error to process request",
        )
    return new_team


@router.get("/", response_model=TeamList)
def get_teams(
    skip: int = 0,
    limit: int = 100,
    name: str = "",
    code: str = "",
    session: Session = Depends(get_session),
):
    teams: list[Team] = session.scalars(
        select(Team)
        .offset(skip)
        .limit(limit)
        .where(Team.name.contains(name) & Team.code.contains(code))
        .order_by(Team.name)
    ).all()
    return {"teams": teams}


@router.get("/{team_id}", response_model=TeamModel)
def get_team(
    team_id: int,
    session: Session = Depends(get_session),
):
    record = session.scalar(select(Team).where(Team.id == team_id))
    if not record:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Team not found"
        )

    return record


@router.put("/{team_id}", response_model=TeamModel)
def update_team(
    team_id: int,
    team: TeamBase,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(select(Team).where(Team.id == team_id))
        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Team not found"
            )

        update_object(record, team.model_dump(exclude_unset=True))
        session.commit()
        session.refresh(record)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return record


@router.delete("/{team_id}", response_model=Message)
def delete_team(team_id: int, session: Session = Depends(get_session)):
    try:
        record = session.scalar(select(Team).where(Team.id == team_id))

        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Team not found",
            )

        session.delete(record)
        session.commit()

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return {"message": "Team deleted"}
