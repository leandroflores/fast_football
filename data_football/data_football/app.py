from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from data_football.schemas import (
    Message,
    UserBase,
    UserDB,
    UserList,
    UserPublic,
)

app: FastAPI = FastAPI()

database: list[dict] = []


@app.get("/", response_model=Message)
def home():
    return {"message": "Olá Mundo!"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserBase):
    user_model: UserDB = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_model)

    return user_model


@app.get("/users/", response_model=UserList)
def get_users():
    return {"users": database}


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserBase):
    if user_id < 0 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    user_model: UserDB = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_model

    return user_model
