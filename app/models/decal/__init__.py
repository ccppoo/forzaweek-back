from app.models.decal.base import DecalBase
from app.models.decal.fh5 import Decal_FH5

__all__ = ("DecalBase", "Decal_FH5", "dbInit")

dbInit = (DecalBase, Decal_FH5)
