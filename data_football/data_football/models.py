from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry: registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class Stadium:
    __tablename__ = "stadiums"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    capacity: Mapped[int]
    city: Mapped[str]
    country: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class Championship:
    __tablename__ = "championships"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    format: Mapped[str]
    context: Mapped[str]
    country: Mapped[str]
    start_year: Mapped[int]
    end_year: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    rounds: Mapped[list["Round"]] = relationship(
        init=False,
        back_populates="championship",
        cascade="all, delete-orphan",
    )


@table_registry.mapped_as_dataclass
class Team:
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[Optional[str]]
    code: Mapped[str] = mapped_column(unique=True)
    country: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


@table_registry.mapped_as_dataclass
class Round:
    __tablename__ = "rounds"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    phase: Mapped[str]
    details: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    championship_id: Mapped[int] = mapped_column(
        ForeignKey("championships.id")
    )

    championship: Mapped[Championship] = relationship(
        init=False, back_populates="rounds"
    )
