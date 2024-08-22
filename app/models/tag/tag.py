from __future__ import annotations
from beanie import Document, Indexed, Link, BackLink

from bson.dbref import DBRef
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Literal, Union
from app.models.i18n import i18n
from app.types.http import Url
from pprint import pprint
from .base import (
    TagBase,
    TagHorizontal,
    TagVertical,
    TagDescription,
    i18nModelDump,
    TagName,
)
from .category import TagCategory

__all__ = ("TagItem",)


class TagItem(TagHorizontal, TagVertical, TagBase):
    # name: List[Link[TagName]] = Field([])
    # image_url: Optional[Url] = Field(None)  # 태그 설명하는 작은 이미지
    # description: List[Link[TagDescription]] = Field([])  # 태그 설명란

    # merged_to: Optional[Link["TagBase"]] = Field(default=None)
    # merged_from: List[Link["TagBase"]] = Field(default=[])

    # parent: Optional[Link["TagBase"]] = Field(default=None)  # 상위 개념
    # children: List[Link["TagBase"]] = Field(default=[])

    category: Optional[Link[TagCategory]] = Field(default=None)  # 태그 종류 분류

    @classmethod
    async def merge(cls, from_: TagItem, to_: TagItem):
        from_.merged_to = to_
        to_.merged_from.append(from_)
        await from_.save_changes()
        await to_.save_changes()
        return

    async def fetch_all_links(self):
        await self.fetch_link("name")
        await self.fetch_link("description")

    async def to_front(self):
        await self.fetch_link("name")

    async def dump(self):
        """
        모든 정보 반환하는 용도 JSON으로 프런트로 보내줄 때 사용
        """
        data = await super().dump()
        data.update(self.get_all_relations())
        await self.fetch_link("category")
        data["category"] = await self.category.dump() if self.category else None
        return data

    def get_all_relations(self):
        mr = self.get_merge_relation()
        vr = self.get_vertical_relation()

        return {**mr, **vr}

    class Settings:
        name: str = "tagItem"
        use_state_management = True
