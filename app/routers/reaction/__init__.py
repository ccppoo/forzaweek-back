from fastapi import APIRouter
from .FH5 import router as FH5Router


__all__ = ("router",)

router = APIRouter(prefix="/reaction", tags=["reaction", "vote", "fav"])

router.include_router(FH5Router, prefix="/FH5")
