from __future__ import annotations
from app.models.deps.system import PostWithImage
from app.models.deps.xbox import SharingCreativeWorks, ForzaHorizonDecal
from ..base import FH5DocumentBase
from pydantic.alias_generators import to_snake
from pprint import pprint
from pydantic import BaseModel, Field


class Decal(ForzaHorizonDecal, PostWithImage, FH5DocumentBase):

    # base_car: Link[CarOriginal]
    # share_code: str = Field(min_length=9, max_length=9)
    # gamer_tag: str = Field()

    # uploader: str
    # image_urls: List[Url] = Field(default=[])

    @staticmethod
    def from_camelCase(data: dict) -> Decal:
        snake_named = {to_snake(k): v for k, v in data.items()}
        pprint(snake_named)
        return Decal(**snake_named)

    class Settings:
        name = "FH5.Decal"
        is_root = True
