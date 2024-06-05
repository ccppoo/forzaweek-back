"""Tuning models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Link
from pydantic import BaseModel, EmailStr, Field
from typing import Literal, List
import pymongo
from .car import Car
from .stat import FH5_Stat
from .tag import Tag

__all__ = ("TuningFH5", "dbInit")


class Tuning(BaseModel):
    creator: str
    tags: List[Link[Tag]] = Field(default=[])


class TuningFH5(Tuning, FH5_Stat):
    """FH5 Tuning DB representation."""

    pass


dbInit = (TuningFH5,)
