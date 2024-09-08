from fastapi import APIRouter

from .api import router as stadiums_router

router: APIRouter = APIRouter(
    prefix="/stadiums",
    tags=["Stadiums"],
)
router.include_router(stadiums_router)
