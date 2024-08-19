from fastapi import APIRouter
from .tags import router as tagRouter

router = APIRouter(prefix="/tags", tags=["tags"])

router.include_router(tagRouter)
