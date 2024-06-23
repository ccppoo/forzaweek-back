from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Literal
from .i18n import i18n

__all__ = ["Tag", "TagName", "TagDescription", "dbInit"]


class TagName(i18n):
    # value : str
    # lang: str
    pass


class TagDescription(i18n):
    # value : str
    # lang: str

    def is_empty(self) -> bool:
        if not self.value:
            return True
        return False


class Tag(Document):

    name: List[Link[TagName]]
    name_en: str

    description: List[Link[TagDescription]]
    kind: Literal["car", "track", "tuning", "decal"] = Field(default=None)

    mergedTo: Optional[Link["Tag"]] = Field(default=None)

    def to_json_all_lang(self):
        names = [
            x.model_dump(
                include=["value", "lang"],
            )
            for x in self.name
        ]
        descriptions = [
            x.model_dump(
                include=["value", "lang"],
            )
            for x in self.description
        ]
        # 직접 id 가져오는 방법?
        _id = self.model_dump(include=["id"])["id"]

        # mergedToTag = mergedTo

        return {
            "id": _id,
            "name": names,
            "name_en": self.name_en,
            "description": descriptions,
            "kind": self.kind,
            "mergedTo": self.mergedTo,
        }

    class Settings:
        name: str = "tag"
        use_state_management = True
        is_root = True


dbInit = (Tag, TagName, TagDescription)
