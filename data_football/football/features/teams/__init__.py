from fastapi import APIRouter

from .api import router as teams_router

router: APIRouter = APIRouter(
    prefix="/teams",
    tags=["Teams"],
)
router.include_router(teams_router)
