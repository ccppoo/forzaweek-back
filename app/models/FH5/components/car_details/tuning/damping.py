from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field
from typing import Literal, List

__all__ = ("Damping",)


class Stiffness(BaseModel):
    front: float = Field(ge=0, le=100)
    rear: float = Field(ge=0, le=100)


class Damping(BaseModel):
    reboundStiffness: Stiffness
    bumpStiffness: Stiffness
