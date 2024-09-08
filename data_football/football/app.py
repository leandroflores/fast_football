from fastapi import FastAPI

from football.domain.entities import (
    Message,
)
from football.features import (
    championships,
    rounds,
    stadiums,
    teams,
    users,
)

app: FastAPI = FastAPI()

app.include_router(championships.router)
app.include_router(rounds.router)
app.include_router(stadiums.router)
app.include_router(teams.router)
app.include_router(users.router)


@app.get("/", response_model=Message)
def home():
    return {"message": "Data Football Service!"}
