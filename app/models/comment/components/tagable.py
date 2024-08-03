from __future__ import annotations
from datetime import datetime
from typing import Any, List, Optional
from beanie import Document, Link
from pydantic import BaseModel, Field
from app.models.i18n import i18n
from app.types.http import Url
from app.models.components import Vote
from app.utils.time import datetime_utc
from app.models.tag import Tag

__all__ = ("Tagable",)


class Tagable(BaseModel):

    # Car, Track, Tuning, Decal 에 직접 태그 추가하면서 붙이는 댓글
    tags: List[Link[Tag]] = Field(default=[])

    async def add_tag(self):
        assert NotImplementedError("Tagable::add_tag not implemented")

    async def remove_tag(self):
        assert NotImplementedError("Tagable::add_tag not implemented")
