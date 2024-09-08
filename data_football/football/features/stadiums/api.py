import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from psycopg import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from football.adapters.database import get_session
from football.adapters.models import Stadium
from football.domain.entities import (
    Message,
    StadiumBase,
    StadiumList,
    StadiumModel,
)
from football.utils import update_object

router: APIRouter = APIRouter()
logger: logging.Logger = logging.getLogger(__name__)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=StadiumModel)
def create_stadium(
    stadium: StadiumBase,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(
            select(Stadium).where(Stadium.name == stadium.name)
        )
        if record:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Stadium '{stadium.name}' already exists",
            )

        new_stadium: Stadium = Stadium(**stadium.model_dump())

        session.add(new_stadium)
        session.commit()
        session.refresh(new_stadium)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Error to process request",
        )
    return new_stadium


@router.get("/", response_model=StadiumList)
def get_stadiums(
    skip: int = 0,
    limit: int = 100,
    name: str = "",
    country: str = "",
    session: Session = Depends(get_session),
):
    stadiums: list[Stadium] = session.scalars(
        select(Stadium)
        .offset(skip)
        .limit(limit)
        .where(Stadium.name.contains(name) & Stadium.country.contains(country))
        .order_by(Stadium.name)
    ).all()
    return {"stadiums": stadiums}


@router.get("/{stadium_id}", response_model=StadiumModel)
def get_stadium(
    stadium_id: int,
    session: Session = Depends(get_session),
):
    record = session.scalar(select(Stadium).where(Stadium.id == stadium_id))
    if not record:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Stadium not found"
        )

    return record


@router.put("/{stadium_id}", response_model=StadiumModel)
def update_stadium(
    stadium_id: int,
    stadium: StadiumBase,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(
            select(Stadium).where(Stadium.id == stadium_id)
        )
        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Stadium not found"
            )

        update_object(record, stadium.model_dump(exclude_unset=True))
        session.commit()
        session.refresh(record)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return record


@router.delete("/{stadium_id}", response_model=Message)
def delete_stadium(
    stadium_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(
            select(Stadium).where(Stadium.id == stadium_id)
        )

        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Stadium not found"
            )

        session.delete(record)
        session.commit()

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return {"message": "Stadium deleted"}
