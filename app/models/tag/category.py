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

    async def name_id_image(self, with_id: bool = True):

        name = (await self.model_dump_name()).model_dump()
        data = {
            "name": name,
            "image_url": self.image_url,
        }
        if with_id:
            data.update(id=str(self.id))
        return data

    async def get_parents(self, limit: int = 5):
        parent_data = None
        if self.parent and limit > 0:
            if isinstance(self.parent, Link):
                await self.fetch_link("parent")
            parent_data = await self.parent.get_parents(limit - 1)

        _name_id_image: dict = await self.name_id_image()
        _name_id_image.update(parent=parent_data)

        return _name_id_image

    async def for_search_result(self):
        """
        태그 검색했을 때 반환하는 결과물로 id, name, category(name, id, image_url), parent(name, id, image_url) 반환
        """
        # _name_id_image: dict = await self.name_id_image()
        me_and_parent = await self.get_parents()

        return me_and_parent

    class Settings:
        name: str = "category"
        use_state_management = True
