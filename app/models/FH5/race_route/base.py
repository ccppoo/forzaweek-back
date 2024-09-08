from app.models.deps.system import HasMultipleImages

from ..base import FH5DocumentBase
from beanie import Link
from pydantic import BaseModel, Field
from typing import List, Literal
from .i18n import RaceRouteName, RaceRouteDescription, RaceRouteNameTranslated
from ..components.image.coordinate_image import CoordinateImage
from ..components.image.full_path_image import FullPathImage
from app.models.i18n import i18n as I18N
from app.types.http import Url


class RaceRouteBase(HasMultipleImages, FH5DocumentBase):

    # image_urls: List[Url] = Field(default=[])
    # first_image: Optional[Url] = Field(default=None)
    full_path_image: FullPathImage
    coordinate_images: List[CoordinateImage] = Field([])
    icon_url: Url

    name: List[Link[RaceRouteName]] = Field([])
    name_translated: List[Link[RaceRouteNameTranslated]] = Field([])
    description: List[Link[RaceRouteDescription]] = Field([])

    en: str

    async def fetch_name_descriptions(self):
        await self.fetch_link("name")
        await self.fetch_link("description")
        await self.fetch_link("name_translated")

    def _prepare_names(self) -> dict:
        names = {}
        for _name in self.name:
            names.update(_name.as_lang_key())
        return names

    def _prepare_names_translated(self) -> dict:
        names_translated = {}
        for _name_translated in self.name_translated:
            names_translated.update(_name_translated.as_lang_key())
        return names_translated

    def _prepare_descriptions(self) -> dict:
        descriptions = {}
        for _description in self.description:
            descriptions.update(_description.as_lang_key())
        return descriptions

    class Settings:
        name = "FH5.RaceRoute"
        is_root = True
