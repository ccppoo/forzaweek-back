from .base import CarBase
from beanie import Link
from pydantic import BaseModel, Field
from typing import List
from .i18n import CarName, CarAlias
from app.models.deps.system import HasMultipleImages
from typing import TYPE_CHECKING

# if TYPE_CHECKING:
from app.models.manufacturer import Manufacturer


__all__ = ("Car",)


class Car(HasMultipleImages, CarBase):

    # image_urls: List[Url] = Field(default=[])
    # first_image: Optional[Url] = Field(default=None)
    name: List[Link[CarName]] = Field([])
    alias: List[Link[CarAlias]] = Field([])

    manufacturer: Link[Manufacturer]  # 국가 추출해서

    production_year: int = Field(ge=1900)
    engine_type: str
    body_style: List[str] = Field([])
    door: int = Field(ge=0)

    class Settings:
        name = "Car"
