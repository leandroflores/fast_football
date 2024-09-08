# import logging
# from http import HTTPStatus

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy import select
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import Session

# from football.adapters.database import get_session
# from football.adapters.models import Player, Team
# from football.domain.entities import (
#     Message,
#     PlayerBase,
#     PlayerList,
#     PlayerModel,
# )
# from football.utils import update_object

# router: APIRouter = APIRouter()
# logger: logging.Logger = logging.getLogger(__name__)


# @router.post("/", status_code=HTTPStatus.CREATED, response_model=PlayerModel)
# def create_player(
#     player: PlayerBase,
#     session: Session = Depends(get_session),
# ):
#     try:
#         team = session.scalar(
#             select(Team).where(Team.id == player.current_team_id)
#         )

#         if not team:
#             raise HTTPException(
#                 status_code=HTTPStatus.NOT_FOUND,
#                 detail="Current Team not found",
#             )

#         new_player: Player = Player(**player.model_dump())
#         new_player.current_team = team

#         session.add(new_player)
#         session.commit()
#         session.refresh(new_player)

#     except IntegrityError:
#         session.rollback()
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST,
#             detail="Integrity error to process request",
#         )
#     return new_player


# @router.get("/", response_model=PlayerList)
# def get_players(
#     skip: int = 0,
#     limit: int = 100,
#     name: str = "",
#     team_id: int = None,
#     session: Session = Depends(get_session),
# ):
#     players: list[Player] = session.scalars(
#         select(Player)
#         .offset(skip)
#         .limit(limit)
#         .where(Player.name.contains(name) & Player.current_team_id == team_id)
#         .order_by(Player.name)
#     ).all()
#     return {"players": players}


# @router.get("/{player_id}", response_model=PlayerModel)
# def get_player(
#     player_id: int,
#     session: Session = Depends(get_session),
# ):
#     record = session.scalar(select(Player).where(Player.id == player_id))
#     if not record:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail="Player not found"
#         )

#     return record


# @router.put("/{player_id}", response_model=PlayerModel)
# def update_player(
#     player_id: int,
#     player: PlayerBase,
#     session: Session = Depends(get_session),
# ):
#     try:
#         record = session.scalar(select(Player).where(Player.id == player_id))
#         if not record:
#             raise HTTPException(
#                 status_code=HTTPStatus.NOT_FOUND,
#                 detail="Player not found",
#             )

#         team = session.scalar(
#             select(Team).where(Team.id == player.current_team_id)
#         )
#         if not team:
#             raise HTTPException(
#                 status_code=HTTPStatus.NOT_FOUND,
#                 detail="Current Team not found",
#             )

#         update_object(record, player.model_dump(exclude_unset=True))
#         record.current_team = team

#         session.commit()
#         session.refresh(record)

#     except IntegrityError:
#         session.rollback()
#         raise HTTPException(
#             HTTPStatus.INTERNAL_SERVER_ERROR,
#             detail="Integrity error to process request",
#         )

#     return record


# @router.delete("/{player_id}", response_model=Message)
# def delete_player(
#     player_id: int,
#     session: Session = Depends(get_session),
# ):
#     try:
#         record = session.scalar(select(Player).where(Player.id == player_id))

#         if not record:
#             raise HTTPException(
#                 status_code=HTTPStatus.NOT_FOUND,
#                 detail="Player not found",
#             )

#         session.delete(record)
#         session.commit()

#     except IntegrityError:
#         session.rollback()
#         raise HTTPException(
#             HTTPStatus.INTERNAL_SERVER_ERROR,
#             detail="Integrity error to process request",
#         )

#     return {"message": "Player deleted"}
