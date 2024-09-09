from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)


class Message(BaseModel):
    message: str


class Model(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserPublic(Model):
    name: str
    email: EmailStr


class UserModel(Model, UserBase): ...


class UserList(BaseModel):
    users: list[UserPublic]


class StadiumBase(BaseModel):
    name: str
    capacity: int
    city: str
    country: str


class StadiumModel(Model, StadiumBase): ...


class StadiumList(BaseModel):
    stadiums: list[StadiumModel]


class ChampionshipBase(BaseModel):
    name: str
    format: str
    context: str
    country: str
    start_year: int
    end_year: int


class ChampionshipModel(Model, ChampionshipBase): ...


class ChampionshipList(BaseModel):
    championships: list[ChampionshipModel]


class TeamBase(BaseModel):
    name: str
    full_name: str = None
    code: str
    country: str


class TeamModel(Model, TeamBase): ...


class TeamList(BaseModel):
    teams: list[TeamModel]


class RoundBase(BaseModel):
    phase: str
    details: str = None
    championship_id: int


class RoundModel(Model, RoundBase): ...


class RoundList(BaseModel):
    rounds: list[RoundModel]


class MatchBase(BaseModel):
    date_hour: str
    goals_home: int
    goals_away: int
    extra_time: bool = False
    goals_extra_time_home: int = 0
    goals_extra_time_away: int = 0
    penalty: bool = False
    goals_penalty_home: int = 0
    goals_penalty_away: int = 0
    stadium_id: int
    round_id: int
    home_team_id: int
    away_team_id: int


class MatchModel(Model, MatchBase): ...


class MatchList(BaseModel):
    matches: list[MatchModel]


class PlayerBase(BaseModel):
    name: str
    full_name: str
    country: str
    birth_date: datetime = None
    current_team_id: int


class PlayerModel(Model, PlayerBase): ...


class PlayerList(BaseModel):
    players: list[PlayerModel]


class GoalBase(BaseModel):
    minute: int
    owngoal: bool = False
    match_id: int
    team_id: int
    player_id: int


class GoalModel(Model, GoalBase): ...


class GoalList(BaseModel):
    goals: list[GoalModel]
