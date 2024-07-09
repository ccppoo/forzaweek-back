from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field
from typing import Literal, List

__all__ = ("Tiers",)


class TierPressure(BaseModel):
    # PSI
    front: float = Field(ge=0, le=100)
    rear: float = Field(ge=0, le=100)


class Tiers(BaseModel):
    pressure: TierPressure
