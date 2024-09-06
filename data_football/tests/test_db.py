from sqlalchemy import select

from data_football.models import User


def test_create_user(session):
    new_user = User(name="alice", password="secret", email="teste@test")
    session.add(new_user)
    session.commit()

    user: User = session.scalar(select(User).where(User.name == "alice"))

    assert user.name == "alice"
    assert user.email == "teste@test"
    assert user.password == "secret"
