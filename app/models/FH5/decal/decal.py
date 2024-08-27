from app.models.deps.system import PostWithImage
from app.models.deps.xbox import SharingCreativeWorks, ForzaHorizonDecal
from ..base import FH5DocumentBase

from pydantic import BaseModel, Field


class Decal(ForzaHorizonDecal, PostWithImage, FH5DocumentBase):

    # base_car: Link[CarOriginal]
    # share_code: str = Field(min_length=9, max_length=9)
    # gamer_tag: str = Field()

    # uploader: str
    # image_urls: List[Url] = Field(default=[])
    # first_image: Optional[Url] = Field(default=None)

    class Settings:
        name = "FH5.Decal"
        is_root = True
