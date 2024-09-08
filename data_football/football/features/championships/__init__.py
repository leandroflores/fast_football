from fastapi import APIRouter

from .api import router as championships_router

router: APIRouter = APIRouter(
    prefix="/championships",
    tags=["Championships"],
)
router.include_router(championships_router)
