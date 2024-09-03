from beanie import Document, Link
from .i18n import CountryName
from pydantic import Field
from .base import CountryBase
from typing import List, Literal
from app.models.deps.system import HasSingleImage

__all__ = ("Country",)


class Country(HasSingleImage, CountryBase):
    """Country DB representation."""

    # image_url: Url = Field()
    en: str
    name: List[Link[CountryName]] = Field([])

    async def as_json(self) -> dict:
        if self.links_not_fetched:
            await self.fetch_all_links()
        names = self._prepare_name()
        return {
            "id": self.id_str,
            "imageURL": self.image_url,
            "name": names,
            "en": self.en,
        }

    async def for_indexedDB(self):
        _country = await self.as_json()
        return _country.pop("en")

    def _prepare_name(self) -> dict:
        """
        returns {
            'en' : 'Korea',
            'ko' : '한국', ...
        }
        """
        names = {}
        for _name in self.name:
            names.update(_name.as_lang_key())
        return names

    @property
    def links_not_fetched(self) -> bool:
        for _name in self.name:
            if isinstance(_name, Link):
                return True
        return False

    # def to_indexedDB(self) -> dict[str, Any]:
    #     name = {x.lang: x.value for x in self.name}

    #     # 직접 id 가져오는 방법?
    #     _id = self.model_dump(include=["id"])["id"]

    #     return {
    #         "id": _id,
    #         "name_en": self.name_en,
    #         "name": name,
    #         "imageURL": self.imageURL,
    #     }

    class Settings:
        name = "country"
