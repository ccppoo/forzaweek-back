from fastapi import APIRouter
from .decal import router as decalRouter


__all__ = ("router",)

router = APIRouter(prefix="", tags=["FH5"])
router.include_router(decalRouter, prefix="/decal")
