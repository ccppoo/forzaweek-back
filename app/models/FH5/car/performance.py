from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field
from typing import Literal, List


class FH5_performance(BaseModel):

    # performance
    speed: float = Field(default=0, ge=0, le=10)
    handling: float = Field(default=0, ge=0, le=10)
    acceleration: float = Field(default=0, ge=0, le=10)
    launch: float = Field(default=0, ge=0, le=10)
    braking: float = Field(default=0, ge=0, le=10)
    offroad: float = Field(default=0, ge=0, le=10)
