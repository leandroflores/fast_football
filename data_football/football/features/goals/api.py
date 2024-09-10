import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from football.adapters.database import get_session
from football.adapters.models import (
    Goal,
    Match,
    Player,
)
from football.domain.entities import (
    GoalBase,
    GoalList,
    GoalModel,
    Message,
)
from football.utils import update_object

router: APIRouter = APIRouter()
logger: logging.Logger = logging.getLogger(__name__)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=GoalModel)
def create_goal(
    goal: GoalBase,
    session: Session = Depends(get_session),
):
    try:
        match = session.scalars(
            select(Match).where(Match.id == goal.match_id)
        ).first()
        if not match:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Match not found",
            )

        player = session.scalars(
            select(Player).where(Player.id == goal.player_id)
        ).first()
        if not player:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Player not found",
            )

        new_goal: Goal = Goal(**goal.model_dump(exclude_unset=True))
        new_goal.match = match
        new_goal.team = player.current_team
        new_goal.player = player

        session.add(new_goal)
        session.commit()
        session.refresh(new_goal)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Integrity error to process request",
        )
    return new_goal


@router.get("/", response_model=GoalList)
def get_goals(
    match_id: int,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    goals: list[Goal] = session.scalars(
        select(Goal)
        .offset(skip)
        .limit(limit)
        .where((Goal.match_id == match_id))
    ).all()
    return {"goals": goals}


@router.get("/{goal_id}", response_model=GoalModel)
def get_goal(
    goal_id: int,
    session: Session = Depends(get_session),
):
    record = session.scalar(select(Goal).where(Goal.id == goal_id))
    if not record:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Goal not found",
        )

    return record


@router.put("/{goal_id}", response_model=GoalModel)
def update_goal(
    goal_id: int,
    goal: GoalBase,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(select(Goal).where(Goal.id == goal_id))
        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Goal not found",
            )

        match = session.scalars(
            select(Match).where(Match.id == goal.match_id)
        ).first()
        if not match:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Match not found",
            )

        player = session.scalars(
            select(Player).where(Player.id == goal.player_id)
        ).first()
        if not player:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Player not found",
            )

        update_object(record, goal.model_dump(exclude_unset=True))
        record.match = match
        record.team = player.current_team
        record.player = player

        session.commit()
        session.refresh(record)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Integrity error to process request",
        )

    return record


@router.delete("/{goal_id}", response_model=Message)
def delete_goal(
    goal_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(select(Goal).where(Goal.id == goal_id))

        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Goal not found",
            )

        session.delete(record)
        session.commit()

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Integrity error to process request",
        )

    return {"message": "Goal deleted"}
