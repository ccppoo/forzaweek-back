from __future__ import annotations

from beanie import Document, Indexed, Link, BackLink
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Literal, Union, Dict
from app.models.i18n import i18n
from app.types.http import Url
from datetime import datetime
from app.utils.time import datetime_utc

from pydantic import BaseModel

__all__ = (
    "TagName",
    "TagDescription",
    "TagBase",
    "TagHorizontal",
    "TagVertical",
)


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


class i18nModelDump(BaseModel):
    id: str
    unknown: Optional[str] = Field(None)
    en: Optional[str] = Field(None)
    ko: Optional[str] = Field(None)
    jp: Optional[str] = Field(None)

    @staticmethod
    def from_i18n(id: str, i18n_docs: List[i18n]):
        lang = {}
        for i18n_doc in i18n_docs:
            lang[i18n_doc.lang] = i18n_doc.value
        return i18nModelDump(id=id, **lang)


class TagBase(Document):

    # 사용자가 바로 추가하는 태그는 lang : 'unknown'으로
    name: List[Link[TagName]] = Field([])
    image_url: Optional[Url] = Field(None)  # 태그 설명하는 작은 이미지
    description: List[Link[TagDescription]] = Field([])  # 태그 설명란

    ## management
    created_at: datetime = Field(default_factory=datetime_utc)

    async def _model_dump_field(self, name: str) -> i18nModelDump:
        _i18nItems = self.__getattribute__(name)
        if any([isinstance(desc, Link) for desc in _i18nItems]):
            await self.fetch_link(name)
        i18ns: List[Union[TagDescription, TagName]] = self.__getattribute__(name)

        return i18nModelDump.from_i18n(str(self.id), i18ns)

    async def model_dump_name(self) -> i18nModelDump:
        return await self._model_dump_field("name")

    async def model_dump_description(self) -> i18nModelDump:
        return await self._model_dump_field("description")

    async def dump(self) -> Dict:
        """
        모든 정보 반환하는 용도 JSON으로 프런트로 보내줄 때 사용
        """
        data = {}
        await self.fetch_link("name")
        await self.fetch_link("description")
        data["name"] = {}
        for tag_name in self.name:
            tag_name: TagName
            data["name"][tag_name.lang] = tag_name.value
        data["description"] = {}
        for tag_desc in self.description:
            tag_desc: TagDescription
            data["description"][tag_desc.lang] = tag_desc.value
        data["imageURL"] = self.image_url
        return data

    class Settings:
        name: str = "tag"
        is_root = True


class TagHorizontal(BaseModel):

    # 유사어, 같은 의미지만 다른 태그로 편입될 경우 존재는 하지만, merged로 표시됨
    # TODO: add DBRef of Tag Document if merged or have parent-children relation
    merged_to: Optional[Link["TagBase"]] = Field(default=None)
    merged_from: List[Link["TagBase"]] = Field(default=[])

    def get_merge_relation(self):
        merged_from_tags = [str(mf.to_ref().id) for mf in self.merged_from]
        merged_to_tag = str(self.merged_to.to_ref().id) if self.merged_to else None

        return {
            "id": str(self.id),
            "merged_to": merged_to_tag,
            "merged_from": merged_from_tags,
        }


class TagVertical(BaseModel):

    parent: Optional[Link["TagBase"]] = Field(default=None)  # 상위 개념
    children: List[Link["TagBase"]] = Field(default=[])

    def get_parent_relation(self):
        parent_id = str(self.parent.to_ref().id) if self.parent else None

        return {"id": str(self.id), "parent": parent_id}

    def get_children_relation(self):
        children_tags = [str(ct.to_ref().id) for ct in self.children]
        return {"id": str(self.id), "children": children_tags}

    def get_vertical_relation(self):
        pr = self.get_parent_relation()
        cr = self.get_children_relation()

        return {**pr, **cr}
