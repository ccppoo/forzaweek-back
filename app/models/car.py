"""Car models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from .manufacturer import Manufacturer


__all__ = ("Car", "dbInit")

PI_RANKS = ["D", "C", "B", "A", "S1", "S2", "X"]
RARITY_LITERAL = [
    "Common",
    "Rare",
    "Epic",
    "Legendary",
    "Forza Edition",
    "Anniversary Edition",
]


class Car(Document):
    """Car DB representation."""

    name: str
    model: str
    manufacturer: Link[Manufacturer]
    year: int
    driveTrain: str
    engine: str = Field(default="")
    door: int = Field(default=0)
    bodyStyle: str = Field(default="")

    @property
    def created(self) -> datetime | None:
        """Datetime car was created from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        name = "car"


dbInit = (Car,)
