from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from typing import List

__all__ = ["Tag", "CarTag", "TrackTag", "TuningTag", "DifficultyTag"]


class Tag(Document):

    name: str
    alias: List[str] = Field(default=[])

    class Settings:
        is_root = True
        name: str = "tag"


class CarTag(Tag):
    pass


class TrackTag(Tag):
    pass


class TuningTag(Tag):
    pass


class DifficultyTag(Tag):
    pass
