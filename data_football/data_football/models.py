from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

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
