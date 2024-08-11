from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Any
from beanie import Document, Link

__all__ = ("PostBlockDataBase",)


class PostBlockDataBase(BaseModel):
    id: str
    type: str
    tunes: Any = Field(default={})  # 정확히 어떻게 사용되는지 모름

    def is_empty(self) -> bool:
        # to remove empty block
        raise NotImplementedError

    def sanitize(self) -> None:
        # remove XSS scripts
        raise NotImplementedError
