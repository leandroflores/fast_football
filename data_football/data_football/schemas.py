from pydantic import BaseModel, ConfigDict, EmailStr


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


class LeagueBase(BaseModel):
    name: str
    season: str
    format: str
    country: str


class LeagueModel(Model, LeagueBase): ...
