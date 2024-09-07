from pydantic import BaseModel, Field
from typing import Optional, List
from app.types.http import Url

__all__ = ("CoordinateImage",)


class Coordinate(BaseModel):
    x: float
    y: float


class CoordinateImage(BaseModel):
    """
    좌표에 따라 사진 저장하는
    """

    x: float
    y: float
    image_url: Url
