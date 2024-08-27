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
