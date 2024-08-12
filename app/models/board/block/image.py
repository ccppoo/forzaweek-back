from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Set
from beanie import Document, Link
import nh3
from app.services.image import update_file_key
from app.configs import cfSettings
from .base import PostBlockDataBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import UserAuth


__all__ = ("ImageBlockData",)


ALLOWED_TAGS = {"br", "a", "i", "b", "u"}

TEMP_KEY_PREFIX = "user/upload"


class _ImageBlockFile(BaseModel):
    url: str = Field(description="https url")
    # https://fzwcdn.forzaweek.com/user/upload/ded32909-b52d-45f5-aa9f-9205f672e107.png

    @property
    def is_temp_key(self) -> bool:
        # TODO: if image upload is from other sites needs tobe fixed
        key = self.url.removeprefix(cfSettings.URL_BASE).strip("/")
        return key.startswith(TEMP_KEY_PREFIX)


class _ImageBlock(BaseModel):
    caption: str = Field(default="", description="plain text style")
    withBorder: bool = Field(default=False)
    withBackground: bool = Field(default=False)
    stretched: bool = Field(default=False)
    file: _ImageBlockFile


class ImageBlockData(PostBlockDataBase):
    data: _ImageBlock

    def update_image_key(self, user: UserAuth):
        if self.data.file.is_temp_key:
            # 임시로 올린 이미지의 경우 upload/user -> board/post 으로 업로드
            new_key = update_file_key(self.data.file.url, user)
            self.data.file.url = new_key
        return

    def is_empty(self) -> bool:
        return False
        # return len(self.data.text.strip()) < 1

    def sanitize(self) -> None:
        self.data.caption = nh3.clean(self.data.caption, tags=ALLOWED_TAGS)
        return
