from fastapi import APIRouter
from .text import router as textCommentRouter

router = APIRouter(prefix="/comment", tags=["comment"])

router.include_router(textCommentRouter)
