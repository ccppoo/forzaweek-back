from fastapi import APIRouter
from .tag import router as tagRouter

router = APIRouter(prefix="/tag", tags=["tag"])
router.include_router(tagRouter)
