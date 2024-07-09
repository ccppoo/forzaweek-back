from fastapi import APIRouter

from app.models.decal import Decal_FH5

__all__ = ("tuningRouter",)

tuningRouter = APIRouter(prefix="/tuning", tags=["tuning"])


@tuningRouter.get("")
async def get_tuning():
    return 200
