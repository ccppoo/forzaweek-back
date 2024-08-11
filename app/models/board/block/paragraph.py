from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Set
from beanie import Document, Link
import nh3

from .base import PostBlockDataBase

__all__ = ("ParagraphBlockData",)


ALLOWED_TAGS = {"br", "a", "i", "b", "u"}


class _ParagraphBlock(BaseModel):
    text: str = Field(default="", description="HTML style")


class ParagraphBlockData(PostBlockDataBase):
    data: _ParagraphBlock

    def is_empty(self) -> bool:
        return len(self.data.text.strip()) < 1

    def sanitize(self) -> None:
        self.data.text = nh3.clean(self.data.text, tags=ALLOWED_TAGS)
        return
