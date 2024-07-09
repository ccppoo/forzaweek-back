from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field
from typing import Literal, List

__all__ = ("Brake",)


class BreakingForce(BaseModel):
    # Percent
    balance: float = Field(ge=0, le=100)
    pressure: float = Field(ge=0, le=200)


class Brake(BaseModel):
    breakingForce: BreakingForce
