from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import List, Optional

__all__ = ["Tag", "CarTag", "TrackTag", "TuningTag", "DifficultyTag"]

ISO_639 = ["en", "ko"]


class Locale(BaseModel):
    value: str
    alias: List[str] = Field(default=[])


class i18n(BaseModel):
    value: str
    alias: List[str] = Field(default=[])
    ko: Optional[Locale]
