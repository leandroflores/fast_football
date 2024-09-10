from fastapi import APIRouter

from .api import router as goals_router

router: APIRouter = APIRouter(
    prefix="/goals",
    tags=["Goals"],
)
router.include_router(goals_router)
