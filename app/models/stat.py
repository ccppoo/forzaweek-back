from beanie import Document, Indexed, Link
from pydantic import BaseModel, Field
from typing import List, Optional, List, Literal
from .tag import Tag
from .car import Car
from datetime import datetime

__all__ = ("Stat", "FH5_Stat", "dbInit")


class Stat(Document):
    """Stat DB representation."""

    car: Link[Car]

    @property
    def created(self) -> datetime | None:
        """Datetime tuning was created from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        is_root = True


class FH5_Stat(Stat):
    # car : Link[Car]

    PI: int = Field(ge=100, le=999)

    # performance
    speed: float = Field(default=0, ge=0, le=10)
    handling: float = Field(default=0, ge=0, le=10)
    acceleration: float = Field(default=0, ge=0, le=10)
    launch: float = Field(default=0, ge=0, le=10)
    braking: float = Field(default=0, ge=0, le=10)
    offroad: float = Field(default=0, ge=0, le=10)

    # test readings
    drive_train: Optional[Literal["AWD", "FWD", "RWD"]] = Field(default=None)
    kg: Optional[int] = Field(default=None)
    kw: Optional[float] = Field(default=None)
    Lateral_G: Optional[float] = Field(default=None)
    accel_100kh: Optional[float] = Field(default=None)
    accel_100mh: Optional[float] = Field(default=None)

    # meta
    rarity: str = Field()

    @property
    def pi_rank(self) -> Literal["D", "C", "B", "A", "S1", "S2", "X"]:
        if self.PI <= 500:
            return "D"
        if self.PI <= 600:
            return "C"
        if self.PI <= 700:
            return "B"
        if self.PI <= 800:
            return "A"
        if self.PI <= 900:
            return "S1"
        if self.PI <= 998:
            return "S2"
        return "X"

    @property
    def hp(self) -> Optional[float]:
        if self.kw:
            return round(self.kw * 0.746, 2)

    @property
    def ps(self) -> Optional[float]:
        if self.kw:
            return round(self.kw * 0.736, 2)


dbInit = (Stat, FH5_Stat)
