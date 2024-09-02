from .base import ManufacturerBase
from beanie import Link
from pydantic import BaseModel, Field
from typing import List
from .i18n import ManufacturerAlias, ManufacturerName
from app.models.country import Country
from app.models.deps.system import HasSingleImage
from app.models.exceptions import RecursiveFetchException

__all__ = ("Manufacturer",)


class Manufacturer(HasSingleImage, ManufacturerBase):

    # __is_recursive = False

    # image_url
    name: List[Link[ManufacturerName]] = Field([])
    alias: List[Link[ManufacturerAlias]] = Field([])
    en: str

    founded: int = Field(ge=1000, le=9999)
    origin: Link[Country]

    async def as_json(self):
        if self.links_not_fetched:
            await self.fetch_all_links()
        country = await self.origin.as_json()

        return {
            "id": self.id_str,
            "name": self._prepare_name(),
            "alias": self._prepare_alias(),
            "en": self.en,
            "founded": self.founded,
            "image_url": self.image_url,
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

    # async def fetch_all_links(self):
    #     if Manufacturer.__is_recursive:
    #         raise RecursiveFetchException
    #     return await super().fetch_all_links()

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

    class Settings:
        name = "manufacturer"

    # @property
    # def created(self) -> datetime | None:
    #     """Datetime car was created from ID."""
    #     return self.id.generation_time if self.id else None

    # def to_json_all_lang(self, _id: bool = False) -> dict[str, Any]:
    #     i18ns = [x.to_front() for x in self.name]
    #     # 직접 id 가져오는 방법?
    #     _id = self.model_dump(include=["id"])["id"]

    #     if _id:
    #         return {
    #             "id": _id,
    #             "i18n": i18ns,
    #             "name_en": self.name_en,
    #             "origin": self.origin.to_json_all_lang(),
    #             "founded": self.founded,
    #             "imageURL": self.imageURL,
    #         }
    #     return {
    #         "i18n": i18ns,
    #         "name_en": self.name_en,
    #         "origin": self.origin,
    #         "founded": self.founded,
    #         "imageURL": self.imageURL,
    #     }

    # def to_indexedDB(self):
    #     # id: string;
    #     # name: i18n[];
    #     # name_en: string;
    #     # founded: number;
    #     # nation: string; // nation ID
    #     # imageURL: string;
    #     name = {x.lang: x.value for x in self.name}
    #     # 직접 id 가져오는 방법?
    #     _id = self.model_dump(include=["id"])["id"]
    #     _origin_id = self.origin.model_dump(include=["id"])["id"]
    #     return {
    #         "id": _id,
    #         "name": name,
    #         "name_en": self.name_en,
    #         "origin": _origin_id,
    #         "founded": self.founded,
    #         "imageURL": self.imageURL,
    #     }

    # def to_simple(self):
    #     _partial = self.model_dump(include=["id", "name_en", "imageURL"])
    #     _name = [n.to_front() for n in self.name]
    #     return {**_partial, "name": _name}

    # class Settings:
    #     name = "manufacturer"
    #     use_state_management = True
