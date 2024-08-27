from .base import ManufacturerBase
from beanie import Link
from pydantic import BaseModel, Field
from typing import List
from .i18n import ManufacturerAlias, ManufacturerName
from app.models.country import Country
from app.models.deps.system import HasSingleImage

__all__ = ("Manufacturer",)


class Manufacturer(HasSingleImage, ManufacturerBase):

    # manufacturer: Link[Manufacturer]  # 국가 추출해서

    # images: List[Url]
    # first_image: Optional[Url]
    name: List[Link[ManufacturerName]] = Field([])
    alias: List[Link[ManufacturerAlias]] = Field([])

    founded: int = Field(ge=1000, le=9999)
    origin: Link[Country]

    # name_en: str
    # name: List[Link[CarName]]

    # short_name_en: str
    # short_name: List[Link[CarShortName]]

    # fh5: Optional[CarBaseStat_FH5]

    class Settings:
        name = "Manufacturer"
