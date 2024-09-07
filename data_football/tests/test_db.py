from sqlalchemy import select

from data_football import models


def test_create_user(user_model: dict, session):
    # Arrange
    new_user: models.User = models.User(
        name=user_model["name"],
        email=user_model["email"],
        password=user_model["password"],
    )

    # Act
    session.add(new_user)
    session.commit()

    # Assert
    user: models.User = session.scalar(
        select(models.User).where(models.User.name == user_model["name"])
    )

    assert user.name == user_model["name"]
    assert user.email == user_model["email"]
    assert user.password == user_model["password"]
