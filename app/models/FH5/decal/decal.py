from __future__ import annotations
from app.models.deps.system import PostWithImage

# from app.models.deps.xbox import SharingCreativeWorks, ForzaHorizonDecal
from app.models.FH5.car import Car_FH5
from app.models.user import UserAuth
from ..base import FH5DocumentBase
from pydantic.alias_generators import to_snake
from pprint import pprint
from pydantic import BaseModel, Field
from beanie import Link
from app.types.http import Url
from typing import List


# class Decal(ForzaHorizonDecal, PostWithImage, FH5DocumentBase):
class Decal(FH5DocumentBase):

    base_car_FH5: Link[Car_FH5]
    share_code: str = Field(min_length=9, max_length=9)
    gamer_tag: str = Field()
    uploader: Link[UserAuth]  # first uploader of decal

    async def as_json(self):
        if self.uploader_link_not_fetched:
            await self.fetch_link("uploader")
            self.uploader: UserAuth
            uploader_uid = self.uploader.user_id
        base_car_id = str(self.base_car_FH5.to_ref().id)
        return {
            "id": self.id_str,
            "uploadedAt": self.uploaded_at,
            "lastEdited": self.last_edited,
            "shareCode": self.share_code,
            "gamerTag": self.gamer_tag,
            "uploader": uploader_uid,
            "baseCar": base_car_id,
        }

    @property
    def uploader_link_not_fetched(self) -> bool:
        if isinstance(self.uploader, Link):
            return True
        return False

    class Settings:
        name = "FH5_Decal"
        is_root = True
