import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from football.adapters.database import get_session
from football.adapters.models import (
    Match,
    Round,
    Stadium,
    Team,
)
from football.domain.entities import (
    MatchBase,
    MatchList,
    MatchModel,
    Message,
)
from football.utils import update_object

router: APIRouter = APIRouter()
logger: logging.Logger = logging.getLogger(__name__)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=MatchModel)
def create_match(
    match: MatchBase,
    session: Session = Depends(get_session),
):
    try:
        stadium = session.scalars(
            select(Stadium).where(Stadium.id == match.stadium_id)
        ).first()
        if not stadium:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Stadium not found",
            )

        round = session.scalars(
            select(Round).where(Round.id == match.round_id)
        ).first()
        if not round:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Round not found",
            )

        home = session.scalars(
            select(Team).where(Team.id == match.home_team_id)
        ).first()
        if not home:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Home team not found",
            )

        away = session.scalars(
            select(Team).where(Team.id == match.away_team_id)
        ).first()
        if not away:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Away team not found",
            )

        if home.id == away.id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Home team can be different from Away team",
            )

        _match = session.scalars(
            select(Match).where(
                (Match.date_hour == match.date_hour)
                & (Match.stadium_id == match.stadium_id)
                & (Match.round_id == match.round_id)
                & (Match.home_team_id == match.home_team_id)
                & (Match.away_team_id == match.away_team_id)
            )
        ).first()
        if _match:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Match already exists",
            )

        new_match: Match = Match(**match.model_dump(exclude_unset=True))
        new_match.stadium = stadium
        new_match.round = round
        new_match.home_team = home
        new_match.away_team = away

        session.add(new_match)
        session.commit()
        session.refresh(new_match)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Integrity error to process request",
        )
    return new_match


@router.get("/", response_model=MatchList)
def get_matches(
    round_id: int,
    team_id: int,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    matches: list[Match] = session.scalars(
        select(Match)
        .offset(skip)
        .limit(limit)
        .where(
            (Match.round_id == round_id)
            & (
                (Match.home_team_id == team_id)
                | (Match.away_team_id == team_id)
            )
        )
    ).all()
    return {"matches": matches}


@router.get("/{match_id}", response_model=MatchModel)
def get_match(
    match_id: int,
    session: Session = Depends(get_session),
):
    record = session.scalar(select(Match).where(Match.id == match_id))
    if not record:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Match not found",
        )

    return record


@router.put("/{match_id}", response_model=MatchModel)
def update_match(
    match_id: int,
    match: MatchBase,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(select(Match).where(Match.id == match_id))
        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Match not found",
            )

        stadium = session.scalars(
            select(Stadium).where(Stadium.id == match.stadium_id)
        ).first()
        if not stadium:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Stadium not found",
            )

        round = session.scalars(
            select(Round).where(Round.id == match.round_id)
        ).first()
        if not round:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Round not found",
            )

        home = session.scalars(
            select(Team).where(Team.id == match.home_team_id)
        ).first()
        if not home:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Home team not found",
            )

        away = session.scalars(
            select(Team).where(Team.id == match.away_team_id)
        ).first()
        if not away:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Away team not found",
            )

        if home.id == away.id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Home team can be different from Away team",
            )

        update_object(record, match.model_dump(exclude_unset=True))
        record.stadium = stadium
        record.round = round
        record.home_team = home
        record.away_team = away

        session.commit()
        session.refresh(record)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Integrity error to process request",
        )

    return record


@router.delete("/{match_id}", response_model=Message)
def delete_match(
    match_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(select(Match).where(Match.id == match_id))

        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Match not found",
            )

        session.delete(record)
        session.commit()

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Integrity error to process request",
        )

    return {"message": "Match deleted"}
