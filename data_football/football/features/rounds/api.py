import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from football.adapters.database import get_session
from football.adapters.models import Championship, Round
from football.domain.entities import (
    Message,
    RoundBase,
    RoundList,
    RoundModel,
)
from football.utils import update_object

router: APIRouter = APIRouter()
logger: logging.Logger = logging.getLogger(__name__)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=RoundModel)
def create_round(
    round: RoundBase,
    session: Session = Depends(get_session),
):
    try:
        new_round: Round = Round(**round.model_dump())
        championship = session.scalars(
            select(Championship).where(
                Championship.id == round.championship_id
            )
        ).first()
        new_round.championship = championship

        session.add(new_round)
        session.commit()
        session.refresh(new_round)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Integrity error to process request",
        )
    return new_round


@router.get("/", response_model=RoundList)
def get_rounds(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    rounds: list[Round] = session.scalars(
        select(Round).offset(skip).limit(limit)
    ).all()
    return {"rounds": rounds}


@router.get("/{round_id}", response_model=RoundModel)
def get_round(
    round_id: int,
    session: Session = Depends(get_session),
):
    record = session.scalar(select(Round).where(Round.id == round_id))
    if not record:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Round not found"
        )

    return record


@router.put("/{round_id}", response_model=RoundModel)
def update_round(
    round_id: int,
    round: RoundBase,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(select(Round).where(Round.id == round_id))
        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Round not found"
            )

        championship = session.scalar(
            select(Championship).where(
                Championship.id == record.championship_id
            )
        )
        if not championship:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Championship not found",
            )

        update_object(record, round.model_dump(exclude_unset=True))
        record.championship = championship

        session.commit()
        session.refresh(record)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Integrity error to process request",
        )

    return record


@router.delete("/{round_id}", response_model=Message)
def delete_round(
    round_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(select(Round).where(Round.id == round_id))

        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Round not found",
            )

        session.delete(record)
        session.commit()

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Integrity error to process request",
        )

    return {"message": "Round deleted"}
