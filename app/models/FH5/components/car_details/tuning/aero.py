from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field
from typing import Literal, List

__all__ = ("Aero",)


class DownForce(BaseModel):
    # unit -> LB, kg, ...
    front: float = Field(ge=0, le=1000)
    rear: float = Field(ge=0, le=1000)
    unit: str


class Aero(BaseModel):
    downforce: DownForce
