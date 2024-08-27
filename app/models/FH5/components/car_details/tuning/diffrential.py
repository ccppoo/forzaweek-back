from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field
from typing import Literal, List

__all__ = ("Tiers",)


class RearDifferntial(BaseModel):
    # percent, %
    acceleration: float = Field(ge=0, le=100)
    deceleration: float = Field(ge=0, le=100)


class Differntial(BaseModel):
    rear: RearDifferntial
