"""Car models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from .car_stat import CarStat
import pymongo


__all__ = ("Car",)

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
    manufacturer: str
    year: int
    type: str
    rarity: int
    country: str
    value: int
    stat: CarStat

    @property
    def rarity_str(
        self,
    ) -> Literal[
        "Common", "Rare", "Epic", "Legendary", "Forza Edition", "Anniversary Edition"
    ]:
        """string rarity in string"""
        return RARITY_LITERAL[self.rarity - 1]

    @property
    def created(self) -> datetime | None:
        """Datetime car was created from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        name = "cars"
