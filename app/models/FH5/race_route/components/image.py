from pydantic import BaseModel, Field
from typing import Optional, List
from app.types.http import Url

__all__ = (
    "CoordinateImage",
    "FullPathImage",
)


class Coordinate(BaseModel):
    x: float
    y: float


class CoordinateImage(BaseModel):
    """
    좌표에 따라 사진 저장하는
    """

    coordinate: Coordinate
    image_urls: List[Url]


class FullPathImage(BaseModel):
    zoom_out: Optional[Url]
    zoom_in: Optional[Url]
