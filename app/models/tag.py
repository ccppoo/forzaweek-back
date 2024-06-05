from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Literal
from .i18n import i18n

__all__ = ["Tag", "TagName", "TagDescription", "dbInit"]


class TagName(i18n):
    # value : str
    # lang: str
    pass


class TagDescription(i18n):
    # value : str
    # lang: str
    pass


class Tag(Document):

    name: Link[TagName]
    description: Link[TagDescription]
    kind: Literal[
        "car",
        "track",
        "tuning",
    ] = Field(default=None)
    mergedTo: Optional[Link["Tag"]] = Field(default=None)

    class Settings:
        is_root = True
        name: str = "tag"


dbInit = (Tag, TagName, TagDescription)
