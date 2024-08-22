from beanie import Document, Indexed, Link, BackLink
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Literal, Union
from app.models.i18n import i18n
from app.types.http import Url
from .base import (
    TagBase,
    TagHorizontal,
    TagVertical,
    TagName,
    TagDescription,
    i18nModelDump,
)

__all__ = ("TagCategory",)


class TagCategory(TagHorizontal, TagVertical, TagBase):

    # name: List[Link[TagName]] = Field([])
    # image_url: Optional[Url] = Field(None)  # 태그 설명하는 작은 이미지
    # description: List[Link[TagDescription]] = Field([])  # 태그 설명란

    # merged_to: Optional[Link["TagBase"]] = Field(default=None)
    # merged_from: List[Link["TagBase"]] = Field(default=[])

    # parent: Optional[Link["TagBase"]] = Field(default=None)  # 상위 개념
    # children: List[Link["TagBase"]] = Field(default=[])

    async def dump(self):
        """
        모든 정보 반환하는 용도 JSON으로 프런트로 보내줄 때 사용
        """
        data = await super().dump()
        data.update(self.get_all_relations())
        return data

    def get_all_relations(self):
        mr = self.get_merge_relation()
        vr = self.get_vertical_relation()
        return {**mr, **vr}

    class Settings:
        name: str = "category"
        use_state_management = True
