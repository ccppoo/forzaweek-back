from .base import ManufacturerBase
from beanie import Link
from pydantic import BaseModel, Field
from typing import List
from .i18n import ManufacturerAlias, ManufacturerName
from app.models.country import Country
from app.models.deps.system import HasSingleImage
from app.models.exceptions import RecursiveFetchException

# from app.models.base import DocumentBase

__all__ = ("Manufacturer",)


class Manufacturer(HasSingleImage, ManufacturerBase):

    # __is_recursive = False

    # image_url
    name: List[Link[ManufacturerName]] = Field([])
    alias: List[Link[ManufacturerAlias]] = Field([])
    en: str

    founded: int = Field(ge=1000, le=9999)
    origin: Link[Country]

    async def as_json(self, *, origin_as_id: bool = True):
        country = None
        if origin_as_id and self.names_not_fetched:
            await self.fetch_names()
            if isinstance(self.origin, Link):
                country = str(self.origin.to_ref().id)
            else:
                country = self.origin.id_str
        if not origin_as_id and self.links_not_fetched:
            await self.fetch_all_links()
            country = await self.origin.as_json()

        return {
            "id": self.id_str,
            "name": self._prepare_name(),
            # "alias": self._prepare_alias(),
            "en": self.en,
            "founded": self.founded,
            "imageURL": self.image_url,
            "origin": country,
        }

    def _prepare_name(self) -> dict:
        """
        returns {
            'en' : 'Ford',
            'ko' : '포드', ...
        }
        """
        names = {}
        for _name in self.name:
            names.update(_name.as_lang_key())
        return names

    def _prepare_alias(self) -> dict:
        """
        returns {
            'en' : 'Ford',
            'ko' : '포드', ...
        }
        """
        aliases = {}
        for _alias in self.alias:
            aliases.update(_alias.as_lang_key())
        return aliases

    async def fetch_names(self):
        await self.fetch_link("name")
        await self.fetch_link("alias")

    @property
    def links_not_fetched(self) -> bool:
        for _name in self.name:
            if isinstance(_name, Link):
                return True
        for _alias in self.alias:
            if isinstance(_alias, Link):
                return True
        if isinstance(self.origin, Link):
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
        name = "manufacturer"
