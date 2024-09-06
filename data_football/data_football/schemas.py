from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserDB(UserBase):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


class League(BaseModel):
    name: str
    season: str
    format: str
    country: str
