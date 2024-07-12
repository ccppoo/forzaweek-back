from beanie import Document, Indexed, Link, BackLink
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Literal
from app.models.i18n import i18n
from app.types.http import Url

__all__ = ["Tag", "TagName", "TagDescription", "dbInit"]


class TagKindName(i18n):
    # value : str
    # lang: str
    pass


class TagKindDescription(i18n):
    # value : str
    # lang: str

    def is_empty(self) -> bool:
        if not self.value:
            return True
        return False


class TagKind(Document):

    # 태그 종류 최상위 단계
    name: List[Link[TagKindName]]
    name_en: str
    imageURL: Optional[Url]  # 태그가 사진을 가지고 있지 않으면 이걸로 대체
    description: List[Link[TagKindDescription]]  # 태그 설명란

    def to_front(self):
        names = [n.model_dump(exclude=["id", "revision_id"]) for n in self.name]
        descriptions = [
            d.model_dump(exclude=["id", "revision_id"]) for d in self.description
        ]

        return {
            **self.model_dump(exclude=["name", "description", "revision_id"]),
            "name": names,
            "description": descriptions,
        }

    def to_simple(self):
        _partial = self.model_dump(include=["id", "imageURL", "name_en"])
        _name = [n.to_front() for n in self.name]
        return {**_partial, "name": _name}

    class Settings:
        name: str = "tagKind"
        use_state_management = True
        is_root = True


dbInit = (TagKind, TagKindName, TagKindDescription)
