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
    # id
    # name: List[Link[TagName]] = Field([])
    # image_url: Optional[Url] = Field(None)  # 태그 설명하는 작은 이미지
    # description: List[Link[TagDescription]] = Field([])  # 태그 설명란

    # merged_to: Optional[Link["TagItem"]] = Field(default=None)
    # merged_from: List[Link["TagItem"]] = Field(default=[])

    # parent: Optional[Link["TagItem"]] = Field(default=None)  # 상위 개념
    # children: List[Link["TagItem"]] = Field(default=[])

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

    async def name_id_image(self, with_id: bool = True):

        name = (await self.model_dump_name()).model_dump()
        data = {
            "name": name,
            "image_url": self.image_url,
        }
        if with_id:
            data.update(id=str(self.id))
        return data

    async def get_parents(self, depth_limit: int = 5):
        parent_data = None
        if self.parent and depth_limit > 1:
            if isinstance(self.parent, Link):
                await self.fetch_link("parent")
            parent_data = await self.parent.get_parents(depth_limit - 1)

        _name_id_image: dict = await self.name_id_image()
        _name_id_image.update(parent=parent_data)

        return _name_id_image

    async def for_search_result(self, depth_limit: int = 5):
        """
        태그 검색했을 때 반환하는 결과물로 id, name, category(name, id, image_url), parent(name, id, image_url) 반환
        """
        # 1. 병합되었을 경우
        # HALO Infinite -> HALO 이렇게 표시
        data = {}
        if self.merged_to:
            if isinstance(self.merged_to, Link):
                await self.fetch_link("merged_to")
            _merge = await self.merged_to.name_id_image()
            data["merged_to"] = _merge

        parent_data = await self.get_parents(depth_limit)
        data.update(parent_data)

        category_data = None
        if self.category:
            if isinstance(self.category, Link):
                await self.fetch_link("category")

            category_data = await self.category.name_id_image()

        category_data and data.update(category=category_data)

        return data

    def get_all_relations(self):
        mr = self.get_merge_relation()
        vr = self.get_vertical_relation()

        return {**mr, **vr}

    class Settings:
        name: str = "tagItem"
        use_state_management = True
