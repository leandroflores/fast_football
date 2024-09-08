from fastapi import APIRouter

from .api import router as players_router

router: APIRouter = APIRouter(
    prefix="/players",
    tags=["Players"],
)
router.include_router(players_router)
