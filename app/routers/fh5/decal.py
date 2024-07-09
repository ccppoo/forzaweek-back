from fastapi import APIRouter

from app.models.decal import Decal_FH5

__all__ = ("decalRouter",)

decalRouter = APIRouter(prefix="/decal", tags=["decal"])


@decalRouter.get("")
async def get_decal():
    return 200
