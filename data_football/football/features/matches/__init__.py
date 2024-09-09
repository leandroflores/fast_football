from fastapi import APIRouter

from .api import router as matches_router

router: APIRouter = APIRouter(
    prefix="/matches",
    tags=["Matches"],
)
router.include_router(matches_router)
