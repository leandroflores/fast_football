import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from psycopg import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from football.adapters.database import get_session
from football.adapters.models import Championship
from football.domain.entities import (
    ChampionshipBase,
    ChampionshipList,
    ChampionshipModel,
    Message,
)
from football.utils import update_object

router: APIRouter = APIRouter()
logger: logging.Logger = logging.getLogger(__name__)


@router.post(
    "/", status_code=HTTPStatus.CREATED, response_model=ChampionshipModel
)
def create_championship(
    championship: ChampionshipBase,
    session: Session = Depends(get_session),
):
    try:
        new_championship: Championship = Championship(
            **championship.model_dump()
        )

        session.add(new_championship)
        session.commit()
        session.refresh(new_championship)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Error to process request",
        )
    return new_championship


@router.get("/", response_model=ChampionshipList)
def get_championships(
    skip: int = 0,
    limit: int = 100,
    name: str = "",
    country: str = "",
    session: Session = Depends(get_session),
):
    championships: list[Championship] = session.scalars(
        select(Championship)
        .offset(skip)
        .limit(limit)
        .where(
            Championship.name.contains(name)
            & Championship.country.contains(country)
        )
        .order_by(Championship.name)
    ).all()
    return {"championships": championships}


@router.get("/{championship_id}", response_model=ChampionshipModel)
def get_championship(
    championship_id: int,
    session: Session = Depends(get_session),
):
    record = session.scalar(
        select(Championship).where(Championship.id == championship_id)
    )
    if not record:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Championship not found"
        )

    return record


@router.put("/{championship_id}", response_model=ChampionshipModel)
def update_championship(
    championship_id: int,
    championship: ChampionshipBase,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(
            select(Championship).where(Championship.id == championship_id)
        )
        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Championship not found",
            )

        update_object(record, championship.model_dump(exclude_unset=True))
        session.commit()
        session.refresh(record)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return record


@router.delete("/{championship_id}", response_model=Message)
def delete_championship(
    championship_id: int, session: Session = Depends(get_session)
):
    try:
        record = session.scalar(
            select(Championship).where(Championship.id == championship_id)
        )

        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Championship not found",
            )

        session.delete(record)
        session.commit()

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return {"message": "Championship deleted"}
