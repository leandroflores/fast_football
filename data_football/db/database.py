from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from data_football.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
