from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from psycopg import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from data_football.database import get_session
from data_football.models import (
    Championship,
    Round,
    Stadium,
    Team,
    User,
)
from data_football.schemas import (
    ChampionshipBase,
    ChampionshipList,
    ChampionshipModel,
    Message,
    RoundBase,
    RoundList,
    RoundModel,
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
from data_football.utils import update_object

app: FastAPI = FastAPI()


@app.get("/", response_model=Message)
def home():
    return {"message": "Data Football Service!"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserBase, session: Session = Depends(get_session)):
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
        record = session.scalar(
            select(Team).where(
                (Team.name == team.name) | (Team.code == team.code)
            )
        )
        if record:
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


@app.post(
    "/rounds/", status_code=HTTPStatus.CREATED, response_model=RoundModel
)
def create_round(round: RoundBase, session: Session = Depends(get_session)):
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
            status_code=HTTPStatus.NOT_FOUND,
            detail="Error to process request",
        )
    return new_round


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


@app.get("/championships/", response_model=ChampionshipList)
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


@app.get("/teams/", response_model=TeamList)
def get_teams(
    skip: int = 0,
    limit: int = 100,
    name: str = "",
    code: str = "",
    session: Session = Depends(get_session),
):
    teams: list[Team] = session.scalars(
        select(Team)
        .offset(skip)
        .limit(limit)
        .where(Team.name.contains(name) & Team.code.contains(code))
        .order_by(Team.name)
    ).all()
    return {"teams": teams}


@app.get("/rounds/", response_model=RoundList)
def get_rounds(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    rounds: list[Round] = session.scalars(
        select(Round).offset(skip).limit(limit)
    ).all()
    return {"rounds": rounds}


@app.get("/users/{user_id}", response_model=UserPublic)
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


@app.get("/stadiums/{stadium_id}", response_model=StadiumModel)
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


@app.get("/championships/{championship_id}", response_model=ChampionshipModel)
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


@app.get("/teams/{team_id}", response_model=TeamModel)
def get_team(
    team_id: int,
    session: Session = Depends(get_session),
):
    record = session.scalar(select(Team).where(Team.id == team_id))
    if not record:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Team not found"
        )

    return record


@app.get("/rounds/{round_id}", response_model=RoundModel)
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


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int, user: UserBase, session: Session = Depends(get_session)
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
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return record


@app.put("/stadiums/{stadium_id}", response_model=StadiumModel)
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


@app.put("/championships/{championship_id}", response_model=ChampionshipModel)
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


@app.put("/teams/{team_id}", response_model=TeamModel)
def update_team(
    team_id: int,
    team: TeamBase,
    session: Session = Depends(get_session),
):
    try:
        record = session.scalar(select(Team).where(Team.id == team_id))
        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Team not found"
            )

        update_object(record, team.model_dump(exclude_unset=True))
        session.commit()
        session.refresh(record)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return record


@app.put("/rounds/{round_id}", response_model=RoundModel)
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

        update_object(record, round.model_dump(exclude_unset=True))
        session.commit()
        session.refresh(record)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return record


@app.delete("/users/{user_id}", response_model=Message)
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
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return {"message": "User deleted"}


@app.delete("/stadiums/{stadium_id}", response_model=Message)
def delete_stadium(stadium_id: int, session: Session = Depends(get_session)):
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


@app.delete("/championships/{championship_id}", response_model=Message)
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


@app.delete("/teams/{team_id}", response_model=Message)
def delete_team(team_id: int, session: Session = Depends(get_session)):
    try:
        record = session.scalar(select(Team).where(Team.id == team_id))

        if not record:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Team not found",
            )

        session.delete(record)
        session.commit()

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return {"message": "Team deleted"}


@app.delete("/rounds/{round_id}", response_model=Message)
def delete_round(round_id: int, session: Session = Depends(get_session)):
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
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error to process request"
        )

    return {"message": "Round deleted"}
