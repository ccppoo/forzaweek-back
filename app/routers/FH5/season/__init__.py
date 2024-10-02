from fastapi import APIRouter, Depends

from pprint import pprint

__all__ = ("router",)

router = APIRouter(prefix="", tags=["season"])
