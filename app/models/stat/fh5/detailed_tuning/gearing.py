from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field
from typing import Literal, List

__all__ = ("Tiers",)


class GearingStages(BaseModel):
    # PSI
    finalDrive: float = Field(ge=0, le=10)
    # TODO: list item validation & limitaion
    stages: List[float] = Field(default=[])


class Gearing(BaseModel):
    gearing: GearingStages
