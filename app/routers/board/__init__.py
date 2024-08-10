from fastapi import APIRouter
from .post import router as postRouter

__all__ = ("router",)

router = APIRouter(prefix="/board", tags=["board"])

router.include_router(postRouter)
