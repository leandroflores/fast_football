import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from football.adapters.database import get_session
from football.adapters.models import User
from football.domain.entities import (
    Message,
    UserBase,
    UserList,
    UserPublic,
)
from football.utils import update_object

router: APIRouter = APIRouter()
logger: logging.Logger = logging.getLogger(__name__)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(
    user: UserBase,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(select(User).where(User.email == user.email))
        if record:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"User '{user.email}' already exists",
            )

        new_user: User = User(**user.model_dump())

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Integrity error to process request",
        )
    return new_user


@router.get("/", response_model=UserList)
def get_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    users: list[User] = session.scalars(
        select(User).offset(skip).limit(limit)
    ).all()
    return {"users": users}


@router.get("/{user_id}", response_model=UserPublic)
def get_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    record = session.scalar(select(User).where(User.id == user_id))
    if not record:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    return record


@router.put("/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserBase,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(select(User).where(User.id == user_id))
        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="User not found"
            )

        update_object(record, user.model_dump(exclude_unset=True))
        session.commit()
        session.refresh(record)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Integrity error to process request",
        )

    return record


@router.delete("/{user_id}", response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    try:
        record = session.scalar(select(User).where(User.id == user_id))

        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="User not found"
            )

        session.delete(record)
        session.commit()

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Integrity error to process request",
        )

    return {"message": "User deleted"}
