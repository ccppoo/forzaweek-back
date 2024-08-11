from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List
from beanie import Document, Link
import nh3

from .base import PostBlockDataBase

__all__ = ("NestedListBlockData",)
ALLOWED_TAGS = {"br", "a", "i", "b", "u"}


class _NestedListBlockItem(BaseModel):
    content: str = Field(default="")
    items: List[_NestedListBlockItem] = Field(default=[])

    def is_empty(self) -> bool:
        # parent가 empty한데 item이 있을 수 있음
        content_empty = len(self.content.strip()) == 0
        items_empty = len(self.items) == 0 or all(
            [item.is_empty() for item in self.items]
        )
        return content_empty and items_empty

    def sanitize(self) -> None:
        self.content = nh3.clean(self.content, tags=ALLOWED_TAGS)
        for item in self.items:
            item.sanitize()
        return


class _NestedListBlock(BaseModel):
    # Max recursive data depth is 3 (limited from front client)
    # WARNING: _NestedListBlockItem is recursive
    style: str
    items: List[_NestedListBlockItem]

    def sanitize(self) -> None:
        _items = []
        for item in self.items:
            if item.is_empty():
                continue
            item.sanitize()
            _items.append(item)
        self.items = _items


class NestedListBlockData(PostBlockDataBase):
    data: _NestedListBlock

    def is_empty(self) -> bool:
        return len(self.data.items) < 1

    def remove_empty(self) -> None:
        _items = []
        for item in self.data.items:
            if item.is_empty():
                continue
            _items.append(item)
        self.data.items = _items

    def sanitize(self) -> None:
        for item in self.data.items:
            item.sanitize()
        self.remove_empty()
