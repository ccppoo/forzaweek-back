from app.models.deps.system import PostWithImage
from app.models.deps.xbox import ForzaHorizonVinylGroups

# from app.models.deps.xbox.forza_horizon import HasShareCode
from ..base import FH5DocumentBase

from pydantic import BaseModel, Field


class VinylGroups(ForzaHorizonVinylGroups, PostWithImage, FH5DocumentBase):

    # share_code: str = Field(min_length=9, max_length=9)
    # gamer_tag: str = Field()

    # uploader: str
    # image_urls: List[Url] = Field(default=[])
    # first_image: Optional[Url] = Field(default=None)

    class Settings:
        name = "FH5.VinylGroups"
        is_root = True
