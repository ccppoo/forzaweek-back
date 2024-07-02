from beanie import Document, Indexed, Link
from pydantic import BaseModel, Field
from typing import List, Optional, List, Literal
from .tag import Tag
from .car import Car
from datetime import datetime
import app.models.FH5.car as fh5

__all__ = ("Stat", "FH5_Stat", "dbInit")


class StatBase(Document):
    """StatBase DB representation."""

    # FH5, FH4 모두 이거 상속 받기!

    car: Link[Car]

    @property
    def created(self) -> datetime | None:
        """Datetime tuning was created from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        is_root = True


class FH5_Stat(StatBase, fh5.Major_Parts, fh5.Performance, fh5.Test_Readings):
    # car : Link[Car]

    PI: int = Field(ge=100, le=999)

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


dbInit = (StatBase, FH5_Stat)
