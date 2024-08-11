from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from beanie import Document, Link
from .block import *
from datetime import datetime
from app.utils.time import datetime_utc

__all__ = ("Post",)


class PostTitle(BaseModel):
    title: str = Field(default="")


class PostCategory(BaseModel):
    category: str = Field(default="")


class PostVote(BaseModel):
    up: int = Field(default=0, ge=0)
    down: int = Field(default=0, ge=0)


class PostMeta(BaseModel):
    user_id: str = Field(description="작성한 사용자 ID")
    uploaded_at: datetime = Field(default_factory=datetime_utc)
    modified_at: Optional[datetime] = Field(default=None)
    comments: int = Field(default=0)


class PostData(BaseModel):
    # editor.js output data로 나오는 data
    version: str
    time: int = Field(ge=0)  # timestamp - ms
    blocks: List[BlockDataTypes] = Field(default=[])

    def sanitize(self) -> None:
        for block in self.blocks:
            block.sanitize()

    def remove_blank(self) -> None:
        _blocks = []
        for block in self.blocks:
            if block.is_empty():
                continue
            _blocks.append(block)
        self.blocks = _blocks
        return


class Post(PostTitle, PostCategory, PostMeta, Document):

    # title: str = Field(default="")
    # category: str = Field(default="")

    # user_id: str = Field(description="작성한 사용자 ID")
    # uploaded_at: datetime = Field(default_factory=datetime_utc)
    # modified_at: Optional[datetime] = Field(default=None)
    # comments: int = Field(default=0)

    data: PostData
    vote: PostVote = Field(default_factory=PostVote)

    class Settings:
        name = "post"
        use_state_management = True
