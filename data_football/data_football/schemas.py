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
