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

    # Reverses
    matches: Mapped["Match"] = relationship(
        init=False,
        back_populates="stadium",
        cascade="all, delete-orphan",
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

    # Reverses
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

    # Reverses
    home_matches: Mapped[list["Match"]] = relationship(
        "Match",
        init=False,
        foreign_keys="Match.home_team_id",
        back_populates="home_team",
        cascade="all, delete-orphan",
    )
    away_matches: Mapped[list["Match"]] = relationship(
        "Match",
        init=False,
        foreign_keys="Match.away_team_id",
        back_populates="away_team",
        cascade="all, delete-orphan",
    )
    players: Mapped[list["Player"]] = relationship(
        init=False,
        back_populates="current_team",
        lazy="select",
    )
    goals: Mapped[list["Goal"]] = relationship(
        init=False,
        back_populates="team",
        lazy="noload",
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

    # Foreign Keys
    championship_id: Mapped[int] = mapped_column(
        ForeignKey("championships.id")
    )

    # Associations
    championship: Mapped[Championship] = relationship(
        init=False,
        back_populates="rounds",
    )

    # Reverses
    matches: Mapped["Match"] = relationship(
        init=False,
        back_populates="round",
        cascade="all, delete-orphan",
    )


@table_registry.mapped_as_dataclass
class Match:
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    date_hour: Mapped[str]
    goals_home: Mapped[int]
    goals_away: Mapped[int]
    extra_time: Mapped[bool]
    goals_extra_time_home: Mapped[int] = mapped_column(nullable=True)
    goals_extra_time_away: Mapped[int] = mapped_column(nullable=True)
    penalty: Mapped[bool]
    goals_penalty_home: Mapped[int] = mapped_column(nullable=True)
    goals_penalty_away: Mapped[int] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    # Foreign Keys
    stadium_id: Mapped[int] = mapped_column(
        ForeignKey("stadiums.id"), nullable=False
    )
    round_id: Mapped[int] = mapped_column(
        ForeignKey("rounds.id"), nullable=False
    )
    home_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"), nullable=False
    )
    away_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"), nullable=False
    )

    # Associations
    stadium: Mapped[Stadium] = relationship(
        init=False,
        back_populates="matches",
    )
    round: Mapped[Round] = relationship(
        init=False,
        back_populates="matches",
        lazy="select",
    )
    home_team: Mapped[Team] = relationship(
        "Team",
        init=False,
        foreign_keys=[home_team_id],
        back_populates="home_matches",
        lazy="noload",
    )
    away_team: Mapped[Team] = relationship(
        "Team",
        init=False,
        foreign_keys=[away_team_id],
        back_populates="away_matches",
        lazy="noload",
    )

    # Reverses
    goals: Mapped[list["Goal"]] = relationship(
        init=False,
        back_populates="match",
        cascade="all, delete-orphan",
    )


@table_registry.mapped_as_dataclass
class Player:
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    full_name: Mapped[str]
    country: Mapped[str]
    birth_date: Mapped[Optional[str]]

    # Foreign Keys
    current_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"), nullable=False
    )

    # Associations
    current_team: Mapped[Team] = relationship(
        init=False,
        back_populates="players",
        lazy="immediate",
    )

    # Reverses
    goals: Mapped[list["Goal"]] = relationship(
        init=False,
        back_populates="player",
        lazy="noload",
    )


@table_registry.mapped_as_dataclass
class Goal:
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    minute: Mapped[int]
    own_goal: Mapped[bool]

    # Foreign Keys
    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"),
        nullable=False,
    )
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False,
    )
    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
    )

    # Associations
    match: Mapped[Match] = relationship(
        init=False,
        back_populates="goals",
        lazy="select",
    )
    team: Mapped[Team] = relationship(
        init=False,
        back_populates="goals",
        lazy="noload",
    )
    player: Mapped[Player] = relationship(
        init=False,
        back_populates="goals",
        lazy="noload",
    )
