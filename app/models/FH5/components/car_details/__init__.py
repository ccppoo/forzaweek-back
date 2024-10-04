from pydantic import BaseModel, Field
from .FH5_meta import Meta
from .major_parts import MajorParts, DRIVING_SYSTEM
from .performance import Performance
from .PI import PI
from .test_readings import TestReadings
from .tuning import *
from typing import Optional


class StatBase(BaseModel):
    PI: int = Field(ge=100, le=999, alias="pi")
    performance: Optional[Performance]


class CarBaseStat(StatBase):
    meta: Meta


class CarTuningStat(StatBase):
    # PI: int = Field(ge=100, le=999)
    # performance: Performance
    detailedTuning: Optional[DetailedTunings]
    testReadings: Optional[TestReadings]
    tuningMajorParts: MajorParts
