from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from data_football.database import get_session
from data_football.models import User
from data_football.schemas import (
    Message,
    UserBase,
    UserList,
    UserPublic,
)

app: FastAPI = FastAPI()


@app.get("/", response_model=Message)
def home():
    return {"message": "Olá Mundo!"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserBase, session: Session = Depends(get_session)):
    try:
        db_user = session.scalar(select(User).where(User.email == user.email))
        if db_user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="User email already exists",
            )

        new_user: User = User(
            name=user.name, email=user.email, password=user.password
        )

        session.add(new_user)
        session.commit()
        session.refresh

        return new_user
    except Exception:
        session.rollback()


@app.get("/users/", response_model=UserList)
def get_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users: list[User] = session.scalars(
        select(User).offset(skip).limit(limit)
    ).all()
    return {"users": users}


@app.get("/users/{user_id}", response_model=UserPublic)
def get_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    return db_user


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int, user: UserBase, session: Session = Depends(get_session)
):
    try:
        db_user = session.scalar(select(User).where(User.id == user_id))
        if not db_user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="User not found"
            )

        db_user.name = user.name
        db_user.email = user.email
        db_user.password = user.password
        session.commit()
        session.refresh(db_user)

        return db_user
    except Exception:
        session.rollback()


@app.delete("/users/{user_id}", response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    try:
        db_user = session.scalar(select(User).where(User.id == user_id))

        if not db_user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="User not found"
            )

        session.delete(db_user)
        session.commit()

        return {"message": "User deleted"}
    except Exception:
        session.rollback()
