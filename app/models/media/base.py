from __future__ import annotations

from app.models.user import UserAuth
from app.models.base import DocumentBase
from pprint import pprint
from pydantic import BaseModel, Field
from beanie import Link

from app.types.http import Url
from typing import List

__all__ = (
    "UserMediaUploads",
    "Votable",
    "Favoratble",
)


class UserMediaUploads(DocumentBase):

    uploader: Link[UserAuth]  # first uploader of decal

    class Settings:
        name = "UserMediaUploads"
        is_root = True


class Votable(BaseModel):
    up_votes: List[Link[UserAuth]] = Field([])
    down_votes: List[Link[UserAuth]] = Field([])


class Favoratble(BaseModel):
    favs: List[Link[UserAuth]] = Field([])
