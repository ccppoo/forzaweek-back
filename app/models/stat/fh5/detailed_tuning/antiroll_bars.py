from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field
from typing import Literal, List

__all__ = ("AntirollBars",)


class AntirollBarPressure(BaseModel):
    # PSI
    front: float = Field(ge=0, le=100)
    rear: float = Field(ge=0, le=100)
    unit: str


class AntirollBars(BaseModel):
    antirollBars: AntirollBarPressure
