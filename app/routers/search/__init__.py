from fastapi import APIRouter
from .tag import router as tagSearchRouter

router = APIRouter(prefix="/search", tags=["search"])

router.include_router(tagSearchRouter)
