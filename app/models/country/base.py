from datetime import datetime
from typing import List, Any, Optional
from beanie import Document, Link
from app.models.i18n import i18n
from app.types.http import Url
from .i18n import CountryName
from pydantic import Field

__all__ = ("CountryBase",)


class CountryBase(Document):
    """Country DB representation."""

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
        name = "Country"
        use_state_management = True
