from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field
from typing import Literal, List

__all__ = ("Springs",)


class SpringLoad(BaseModel):
    # 스프링 (최대)하중
    # unit -> LB, kg, ...
    front: float = Field(ge=0, le=100_000)
    rear: float = Field(ge=0, le=100_000)
    unit: str


class RideHeight(BaseModel):
    # unit -> Inch, cm,m
    front: float = Field(ge=0, le=100)
    rear: float = Field(ge=0, le=100)
    unit: str


class Springs(BaseModel):
    springs: SpringLoad
    rideHeight: RideHeight
