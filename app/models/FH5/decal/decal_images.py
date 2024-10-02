from __future__ import annotations

from app.models.user import UserAuth
from pprint import pprint
from pydantic import BaseModel, Field
from beanie import Link

from app.types.http import Url
from typing import List, Literal, Union, Mapping
from .decal import Decal
from app.models.media import UserMediaUploads

__all__ = ("DecalImages",)


class DecalImages(UserMediaUploads):
    # uploader: Link[UserAuth]
    decalBase: Link[Decal]  # images that's related to

    images: List[Url] = Field([])

    up_votes: List[str] = Field([])
    down_votes: List[str] = Field([])
    favs: List[str] = Field([])

    async def as_json(self):

        if self.uploader_link_not_fetched:
            await self.fetch_link("uploader")
        uploader_uid = self.uploader.user_id

        return {
            "id": self.id_str,
            "decalBase": self.baseDecalID,
            "uploadedAt": self.uploaded_at,
            "lastEdited": self.last_edited,
            "images": self.images,
            "uploader": uploader_uid,
        }

    async def to_front(self, user: UserAuth | None = None):
        # TODO: mongoDB aggretion으로
        voted = {"up": [], "down": []}
        faved = False
        if user:
            if user.user_id in self.up_votes:
                voted["up"].append(user.user_id)
            if user.user_id in self.down_votes:
                voted["down"].append(user.user_id)
            if user.user_id in self.favs:
                faved = True

        if self.uploader_link_not_fetched:
            await self.fetch_link("uploader")
        uploader_uid = self.uploader.user_id

        return {
            "id": self.id_str,
            "decalBase": self.baseDecalID,
            "uploadedAt": self.uploaded_at,
            "lastEdited": self.last_edited,
            "images": self.images,
            "uploader": uploader_uid,
            "up_votes": len(self.up_votes),
            "down_votes": len(self.down_votes),
            "voted": voted,
            "faved": faved,
        }

    async def get_votes(self, user: UserAuth | None = None):
        # TODO: mongoDB aggretion으로
        voted = {"up": [], "down": []}
        if user:
            if user.user_id in self.up_votes:
                voted["up"].append(user.user_id)
            if user.user_id in self.down_votes:
                voted["down"].append(user.user_id)

        return {
            "id": self.id_str,
            "decalBase": self.baseDecalID,
            "upVotes": len(self.up_votes),
            "downVotes": len(self.down_votes),
            "voted": voted,
        }

    @property
    def baseDecalID(self) -> str:
        if isinstance(self.decalBase, Link):
            return str(self.decalBase.to_ref().id)
        else:
            return self.decalBase.id_str

    @property
    def uploader_link_not_fetched(self) -> bool:
        if isinstance(self.uploader, Link):
            return True
        return False

    @property
    def interactions_not_fetched(self) -> bool:
        for _up_vote in self.up_votes:
            if isinstance(_up_vote, Link):
                return True
        for _down_vote in self.down_votes:
            if isinstance(_down_vote, Link):
                return True
        for _fav in self.favs:
            if isinstance(_fav, Link):
                return True

        return False

    class Settings:
        name = "DecalImageFH5"
