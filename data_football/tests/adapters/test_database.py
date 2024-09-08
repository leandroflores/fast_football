from sqlalchemy.orm import Session


def test_get_session(session: Session):
    # Assert
    assert session.is_active is True
    assert type(session) is Session
