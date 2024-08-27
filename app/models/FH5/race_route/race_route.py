from .base import RaceRouteBase

from app.models.deps.system import HasMultipleImages
from ..components.race_route import TrackCategory, TrackFormat, TrackFullPathImage
from beanie import Link
from pydantic import BaseModel, Field
from typing import List


class RaceRoute(RaceRouteBase):

    # image_urls: List[Url] = Field(default=[])
    # first_image: Optional[Url] = Field(default=None)

    # world: Literal["Mexico", "Hot Wheels", "Rally"]

    # name: List[Link[RaceRouteName]] = Field([])
    # description: List[Link[RaceRouteDescription]] = Field([])
    # name_translated: List[Link[RaceRouteNameTranslated]] = Field([])

    format: TrackFormat
    category: TrackCategory
    full_path_image: TrackFullPathImage
