from typing import List, Optional, Union
from pydantic import Field, BaseModel
from app.types.http import Url
from pprint import pprint

__all__ = (
    "HasMultipleImages",
    "HasSingleImage",
)


class HasMultipleImages(BaseModel):

    image_urls: List[Url] = Field(default=[])
    first_image: Optional[Url] = Field(default=None)


class HasSingleImage(BaseModel):

    image_url: Url = Field()
