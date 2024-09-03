from .base import CarBase
from beanie import Link
from pydantic import BaseModel, Field
from typing import List
from .i18n import CarName, CarAlias
from app.models.i18n import i18n as I18N
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

    async def as_json(self, manufacturer_as_id: bool = True):
        manufacturer = None
        if manufacturer_as_id and self.names_not_fetched:
            await self.fetch_names()
            manufacturer = str(self.manufacturer.to_ref().id)
        if not manufacturer_as_id and self.links_not_fetched:
            await self.fetch_all_links()
            manufacturer = await self.manufacturer.as_json()

        return {
            "id": self.id_str,
            "name": self._prepare_names(),
            "alias": self._prepare_aliases(),
            "imageURLs": self.image_urls,
            "manufacturer": manufacturer,
            "productionYear": self.production_year,
            "engineType": self.engine_type,
            "bodyStyle": self.body_style,
            "door": self.door,
        }

    def _prepare_names(self) -> dict:
        """
        returns {
            'en' : [
                'Ford'
            ],
            'ko' : '포드', ...
        }
        """
        names = {}
        for _name in self.name:
            names = I18N.build_multi_value(names, _name)
        return names

    def _prepare_aliases(self) -> dict:
        """
        returns {
            'en' : 'Ford',
            'ko' : '포드', ...
        }
        """
        aliases = {}
        for _alias in self.alias:
            aliases = I18N.build_multi_value(aliases, _alias)

        return aliases

    async def fetch_names(self):
        await self.fetch_link("name")
        await self.fetch_link("alias")

    async def fetch_manufacturer(self):
        await self.fetch_link("manufacturer")

    @property
    def links_not_fetched(self) -> bool:
        for _name in self.name:
            if isinstance(_name, Link):
                return True
        for _alias in self.alias:
            if isinstance(_alias, Link):
                return True
        if isinstance(self.manufacturer, Link):
            return True
        return False

    @property
    def names_not_fetched(self) -> bool:
        for _name in self.name:
            if isinstance(_name, Link):
                return True
        for _alias in self.alias:
            if isinstance(_alias, Link):
                return True
        return False

    class Settings:
        name = "Car"
