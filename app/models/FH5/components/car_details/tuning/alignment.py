from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field
from typing import Literal, List

__all__ = ("Alignment",)


class CamberAlignment(BaseModel):
    # degree, 도
    front: float = Field(ge=-100, le=100)
    rear: float = Field(ge=-100, le=100)


class ToeAlignment(BaseModel):
    # degree, 도
    front: float = Field(ge=-100, le=100)
    rear: float = Field(ge=-100, le=100)


class CasterAngle(BaseModel):
    # degree, 도
    angle: float = Field(ge=-100, le=100)


class Alignment(BaseModel):
    camber: CamberAlignment
    toe: ToeAlignment
    frontCaster: CasterAngle
