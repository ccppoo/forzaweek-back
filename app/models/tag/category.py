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
from app.models.i18n import i18n as I18N

__all__ = ("TagCategory",)


class TagCategory(TagHorizontal, TagVertical, TagBase):

    # name: List[Link[TagName]] = Field([])
    # image_url: Optional[Url] = Field(None)  # 태그 설명하는 작은 이미지
    # description: List[Link[TagDescription]] = Field([])  # 태그 설명란

    # merged_to: Optional[Link["TagBase"]] = Field(default=None)
    # merged_from: List[Link["TagBase"]] = Field(default=[])

    # parent: Optional[Link["TagBase"]] = Field(default=None)  # 상위 개념
    # children: List[Link["TagBase"]] = Field(default=[])

    async def as_json(self):

        if self.name_not_fetched:
            await self.fetch_link("name")
        if self.description_not_fetched:
            await self.fetch_link("description")

        return {
            "id": self.id_str,
            "name": self._prepare_names(),
            "description": self._prepare_description(),
            "imageURL": self.image_url,
            "mergedTo": self.merged_to_id,
            "mergedFrom": self.merged_from_ids,
            "parent": self.parent_id,
            "children": self.children_ids,
        }

    def _prepare_names(self) -> dict:
        names = {}
        for _name in self.name:
            names.update(_name.as_lang_key())
        return names

    def _prepare_description(self) -> dict:
        descriptions = {}
        for _desc in self.description:
            descriptions.update(_desc.as_lang_key())

        return descriptions

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

    @property
    def name_not_fetched(self) -> bool:
        for _name in self.name:
            if isinstance(_name, Link):
                return True
        return False

    @property
    def description_not_fetched(self) -> bool:
        for _description in self.description:
            if isinstance(_description, Link):
                return True
        return False

    @property
    def merged_to_id(self) -> str | None:
        if not self.merged_to:
            return None
        if self.merged_to:
            if isinstance(self.merged_to, Link):
                return str(self.merged_to.to_ref().id)
            return self.merged_to.id_str

    @property
    def merged_from_ids(self) -> List[str]:
        merged_froms = []
        for _mfrom in self.merged_from:
            if isinstance(_mfrom, Link):
                merged_froms.append(str(_mfrom.to_ref().id))
            else:
                merged_froms.append(_mfrom.id_str)
        return merged_froms

    @property
    def parent_id(self) -> str | None:
        if not self.parent:
            return None
        if isinstance(self.parent, Link):
            return str(self.parent.to_ref().id)
        return self.parent.id_str

    @property
    def children_ids(self) -> List[str]:
        children_ids = []
        for chd in self.children:
            if isinstance(chd, Link):
                children_ids.append(str(chd.to_ref().id))
            else:
                children_ids.append(chd.id_str)
        return children_ids

    class Settings:
        name: str = "category"
        use_state_management = True
