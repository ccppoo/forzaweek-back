from app.models.deps.system import HasMultipleImages

from ..base import FH5DocumentBase
from beanie import Link
from pydantic import BaseModel, Field
from typing import List
from .i18n import RaceRouteName, RaceRouteDescription, RaceRouteNameTranslated
from ..components.world import WorldDependent


class RaceRouteBase(HasMultipleImages, WorldDependent, FH5DocumentBase):

    # image_urls: List[Url] = Field(default=[])
    # first_image: Optional[Url] = Field(default=None)

    # world: Literal["Mexico", "Hot Wheels", "Rally"]

    name: List[Link[RaceRouteName]] = Field([])
    description: List[Link[RaceRouteDescription]] = Field([])
    name_translated: List[Link[RaceRouteNameTranslated]] = Field([])

    class Settings:
        name = "FH5.RaceRoute"
        is_root = True
