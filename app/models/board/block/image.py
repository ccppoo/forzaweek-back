from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Set
from beanie import Document, Link
import nh3

from .base import PostBlockDataBase

__all__ = ("ImageBlockData",)


ALLOWED_TAGS = {"br", "a", "i", "b", "u"}


# const imageBlockData = z.object({
#   caption: z.string({ description: 'plain string' }).default(''),
#   withBorder: z.boolean().default(false),
#   withBackground: z.boolean().default(false),
#   stretched: z.boolean().default(false),
#   file: z.object({
#     url: z.string().url(),
#   }),
# });


class _ImageBlockFile(BaseModel):
    url: str = Field(description="https url")


class _ImageBlock(BaseModel):
    caption: str = Field(default="", description="plain text style")
    withBorder: bool = Field(default=False)
    withBackground: bool = Field(default=False)
    stretched: bool = Field(default=False)
    file: _ImageBlockFile


class ImageBlockData(PostBlockDataBase):
    data: _ImageBlock

    def is_empty(self) -> bool:
        return False
        # return len(self.data.text.strip()) < 1

    def sanitize(self) -> None:
        self.data.caption = nh3.clean(self.data.caption, tags=ALLOWED_TAGS)
        return
