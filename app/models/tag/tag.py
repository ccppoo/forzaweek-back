from beanie import Document, Indexed, Link, BackLink
from bson.dbref import DBRef
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Literal
from app.models.i18n import i18n
from app.types.http import Url
from .kind import TagKind
from pprint import pprint

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
    imageURL: Optional[Url]  # 태그 설명하는 작은 이미지
    description: List[Link[TagDescription]]  # 태그 설명란
    kind: Link[TagKind]  # 태그 종류 분류

    # management
    parentTag: Optional[Link["Tag"]] = Field(default=None)  # 상위 개념
    mergedTo: Optional[Link["Tag"]] = Field(
        default=None
    )  # 유사어, 같은 의미지만 다른 태그로 편입될 경우 존재는 하지만, merged로 표시됨

    # TODO: add DBRef of Tag Document if merged or have parent-children relation
    # childrenTag: List[DBRef] = Field(default=[])
    # mergedFrom: List[DBRef] = Field(default=[])

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

        return {
            "id": _id,
            "name": names,
            "name_en": self.name_en,
            "description": descriptions,
            "kind": self.kind,
            "mergedTo": self.mergedTo,
        }

    def to_front(self):

        names = [n.to_front() for n in self.name]
        pprint(names)
        descriptions = [d.to_front() for d in self.description]
        kind = self.kind.to_front()

        return {
            **self.model_dump(
                include=["id", "imageURL", "name_en", "parentTag", "mergedTo"]
            ),
            "name": names,
            "description": descriptions,
            "kind": kind,
        }

    def to_simple(self):
        _partial = self.model_dump(
            include=[
                "id",
                "imageURL",
                "name",
                "name_en",
                "description",
                "parentTag",
                "childrenTag",
            ]
        )

        names = [n.to_front() for n in self.name]
        descriptions = [d.to_front() for d in self.description]
        kind = self.kind.to_simple()

        return {
            **self.model_dump(
                include=["id", "imageURL", "name_en", "parentTag", "mergedTo"]
            ),
            "name": names,
            "description": descriptions,
            "kind": kind,
        }

    # @field_validator("childrenTag")
    # @classmethod
    # def validate_childrenTag(cls, v):
    #     if isinstance(v, BackLink):
    #         return None
    #     return v

    # @field_validator("mergedFrom")
    # @classmethod
    # def validate_mergedFrom(cls, v):
    #     if isinstance(v, BackLink):
    #         return None
    #     return v

    class Settings:
        name: str = "tag"
        use_state_management = True
        is_root = True


dbInit = (Tag, TagName, TagDescription)
