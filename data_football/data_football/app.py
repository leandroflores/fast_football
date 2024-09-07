from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from psycopg import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from data_football.database import get_session
from data_football.models import (
    Championship,
    Stadium,
    Team,
    User,
)
from data_football.schemas import (
    ChampionshipBase,
    ChampionshipList,
    ChampionshipModel,
    Message,
    StadiumBase,
    StadiumList,
    StadiumModel,
    TeamBase,
    TeamList,
    TeamModel,
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

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Error to process request",
        )
    return new_stadium


@app.post(
    "/championships/",
    status_code=HTTPStatus.CREATED,
    response_model=ChampionshipModel,
)
def create_championship(
    championship: ChampionshipBase, session: Session = Depends(get_session)
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


@app.post("/teams/", status_code=HTTPStatus.CREATED, response_model=TeamModel)
def create_team(team: TeamBase, session: Session = Depends(get_session)):
    try:
        team_record = session.scalar(
            select(Team).where(
                (Team.name == team.name) | (Team.code == team.code)
            )
        )
        if team_record:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Team '{team.name} [{team.code}]' already exists",
            )

        new_team: Team = Team(**team.model_dump())

        session.add(new_team)
        session.commit()
        session.refresh(new_team)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Error to process request",
        )
    return new_team


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


@app.get("/championships/", response_model=ChampionshipList)
def get_championships(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    championships: list[Championship] = session.scalars(
        select(Championship).offset(skip).limit(limit)
    ).all()
    return {"championships": championships}


@app.get("/teams/", response_model=TeamList)
def get_teams(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    teams: list[Team] = session.scalars(
        select(Team).offset(skip).limit(limit)
    ).all()
    return {"teams": teams}


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


@app.get("/championships/{championship_id}", response_model=ChampionshipModel)
def get_championship(
    championship_id: int,
    session: Session = Depends(get_session),
):
    championship_record = session.scalar(
        select(Championship).where(Championship.id == championship_id)
    )
    if not championship_record:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Championship not found"
        )

    return championship_record


@app.get("/teams/{team_id}", response_model=TeamModel)
def get_team(
    team_id: int,
    session: Session = Depends(get_session),
):
    team_record = session.scalar(select(Team).where(Team.id == team_id))
    if not team_record:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Team not found"
        )

    return team_record


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

    except IntegrityError:
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

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return stadium_record


@app.put("/championships/{championship_id}", response_model=ChampionshipModel)
def update_championship(
    championship_id: int,
    championship: ChampionshipBase,
    session: Session = Depends(get_session),
):
    try:
        championship_record = session.scalar(
            select(Championship).where(Championship.id == championship_id)
        )
        if not championship_record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Championship not found",
            )

        championship_record.name = championship.name
        championship_record.format = championship.format
        championship_record.context = championship.context
        championship_record.country = championship.country
        championship_record.start_year = championship.start_year
        championship_record.end_year = championship.end_year
        session.commit()
        session.refresh(championship_record)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return championship_record


@app.put("/teams/{team_id}", response_model=TeamModel)
def update_team(
    team_id: int,
    team: TeamBase,
    session: Session = Depends(get_session),
):
    try:
        team_record = session.scalar(select(Team).where(Team.id == team_id))
        if not team_record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Team not found"
            )

        team_record.name = team.name
        team_record.full_name = team.full_name
        team_record.code = team.code
        team_record.country = team.country
        session.commit()
        session.refresh(team_record)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return team_record


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

    except IntegrityError:
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

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return {"message": "Stadium deleted"}


@app.delete("/championships/{championship_id}", response_model=Message)
def delete_championship(
    championship_id: int, session: Session = Depends(get_session)
):
    try:
        championship_record = session.scalar(
            select(Championship).where(Championship.id == championship_id)
        )

        if not championship_record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Championship not found",
            )

        session.delete(championship_record)
        session.commit()

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return {"message": "Championship deleted"}


@app.delete("/teams/{team_id}", response_model=Message)
def delete_team(team_id: int, session: Session = Depends(get_session)):
    try:
        team_record = session.scalar(select(Team).where(Team.id == team_id))

        if not team_record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Team not found",
            )

        session.delete(team_record)
        session.commit()

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return {"message": "Team deleted"}
