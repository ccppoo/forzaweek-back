from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List
from beanie import Document, Link
import nh3
from .base import PostBlockDataBase

__all__ = ("HeaderBlockData",)

ALLOWED_TAGS = {"br", "a", "i", "b", "u"}


class _HeaderBlock(BaseModel):
    text: str
    level: int = Field(ge=0)


class HeaderBlockData(PostBlockDataBase):
    data: _HeaderBlock

    def is_empty(self) -> bool:
        return len(self.data.text.strip()) < 1

    def sanitize(self) -> None:
        self.data.text = nh3.clean(self.data.text, tags=ALLOWED_TAGS)
