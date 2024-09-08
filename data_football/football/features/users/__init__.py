from fastapi import APIRouter

from .api import router as users_router

router: APIRouter = APIRouter(
    prefix="/users",
    tags=["Users"],
)
router.include_router(users_router)
