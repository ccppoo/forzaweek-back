from beanie import Document, Link
from .i18n import CountryName
from pydantic import Field
from .base import CountryBase
from typing import List
from app.models.deps.system import HasSingleImage

__all__ = ("Country",)


class Country(HasSingleImage, CountryBase):
    """Country DB representation."""

    # image_url: Url = Field()
    en: str
    name: List[Link[CountryName]] = Field([])

    async def as_json(self):
        if self.links_not_fetched:
            await self.fetch_all_links()
        names = self._prepare_name()
        return {
            "id": self.id_str,
            "image_url": self.image_url,
            "name": names,
            "en": self.en,
        }

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

    # @property
    # def created(self) -> datetime | None:
    #     """Datetime car was created from ID."""
    #     return self.id.generation_time if self.id else None

    # def to_json(self, lang: Optional[str]) -> dict[str, Any]:
    #     if lang:
    #         for nationName in self.name:
    #             if nationName.lang == lang:
    #                 return nationName.model_dump(exclude=["id", "revision_id"])
    #     data = []
    #     for nationName in self.name:
    #         nationName: NationName
    #         data.append(nationName.model_dump(exclude=["id", "revision_id"]))
    #     return data

    # def to_json_all_lang(self, _id: bool = False) -> dict[str, Any]:
    #     i18ns = [x.to_front() for x in self.name]
    #     # 직접 id 가져오는 방법?
    #     _id = self.model_dump(include=["id"])["id"]

    #     if _id:

    #         return {
    #             "id": _id,
    #             "i18n": i18ns,
    #             "name_en": self.name_en,
    #             "imageURL": self.imageURL,
    #         }
    #     return {
    #         "i18n": i18ns,
    #         "name_en": self.name_en,
    #         "imageURL": self.imageURL,
    #     }

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
        use_state_management = True
