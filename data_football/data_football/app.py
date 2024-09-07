from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from psycopg import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from data_football.database import get_session
from data_football.models import Stadium, User
from data_football.schemas import (
    Message,
    StadiumBase,
    StadiumList,
    StadiumModel,
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
        user_record = session.scalar(
            select(User).where(User.email == user.email)
        )
        if user_record:
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
            detail="Error to process request",
        )
    return new_user


@app.post(
    "/stadiums/", status_code=HTTPStatus.CREATED, response_model=StadiumModel
)
def create_stadium(
    stadium: StadiumBase, session: Session = Depends(get_session)
):
    try:
        stadium_record = session.scalar(
            select(Stadium).where(Stadium.name == stadium.name)
        )
        if stadium_record:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Stadium '{stadium.name}' already exists",
            )

        new_stadium: Stadium = Stadium(**stadium.model_dump())

        session.add(new_stadium)
        session.commit()
        session.refresh(new_stadium)

    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Error to process request",
        )
    return new_stadium


@app.get("/users/", response_model=UserList)
def get_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users: list[User] = session.scalars(
        select(User).offset(skip).limit(limit)
    ).all()
    return {"users": users}


@app.get("/stadiums/", response_model=StadiumList)
def get_stadiums(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    stadiums: list[Stadium] = session.scalars(
        select(Stadium).offset(skip).limit(limit)
    ).all()
    return {"stadiums": stadiums}


@app.get("/users/{user_id}", response_model=UserPublic)
def get_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    user_record = session.scalar(select(User).where(User.id == user_id))
    if not user_record:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    return user_record


@app.get("/stadiums/{stadium_id}", response_model=StadiumModel)
def get_stadium(
    stadium_id: int,
    session: Session = Depends(get_session),
):
    stadium_record = session.scalar(
        select(Stadium).where(Stadium.id == stadium_id)
    )
    if not stadium_record:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Stadium not found"
        )

    return stadium_record


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int, user: UserBase, session: Session = Depends(get_session)
):
    try:
        user_record = session.scalar(select(User).where(User.id == user_id))
        if not user_record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="User not found"
            )

        user_record.name = user.name
        user_record.email = user.email
        user_record.password = user.password
        session.commit()
        session.refresh(user_record)

    except Exception:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return user_record


@app.put("/stadiums/{stadium_id}", response_model=StadiumModel)
def update_stadium(
    stadium_id: int,
    stadium: StadiumBase,
    session: Session = Depends(get_session),
):
    try:
        stadium_record = session.scalar(
            select(Stadium).where(Stadium.id == stadium_id)
        )
        if not stadium_record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Stadium not found"
            )

        stadium_record.name = stadium.name
        stadium_record.capacity = stadium.capacity
        stadium_record.city = stadium.city
        stadium_record.country = stadium.country
        session.commit()
        session.refresh(stadium_record)

    except Exception:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return stadium_record


@app.delete("/users/{user_id}", response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    try:
        user_record = session.scalar(select(User).where(User.id == user_id))

        if not user_record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="User not found"
            )

        session.delete(user_record)
        session.commit()

    except Exception:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return {"message": "User deleted"}


@app.delete("/stadiums/{stadium_id}", response_model=Message)
def delete_stadium(stadium_id: int, session: Session = Depends(get_session)):
    try:
        stadium_record = session.scalar(
            select(Stadium).where(Stadium.id == stadium_id)
        )

        if not stadium_record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Stadium not found"
            )

        session.delete(stadium_record)
        session.commit()

    except Exception:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return {"message": "Stadium deleted"}
