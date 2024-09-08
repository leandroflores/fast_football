from fastapi import APIRouter

from .api import router as rounds_router

router: APIRouter = APIRouter(
    prefix="/rounds",
    tags=["Rounds"],
)
router.include_router(rounds_router)
