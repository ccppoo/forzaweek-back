from pydantic import BaseModel, Field
from typing import Optional, Literal

__all__ = ("RacingFormat",)


FH5_TRACK_FROMATS = Literal[
    "sprint",
    "trail",
    "course",
    "circuit",
    "scramble",
    "street",
    "cross_country",
    "cross_country_circuit",
]


class TrackFormat(BaseModel):
    """
    sprint, trail, course, circuit, scramble 지칭하는 것들
    """

    format: FH5_TRACK_FROMATS
    laps: Optional[int] = Field(ge=0)  # 0이면 sprint 형태, 1이상이면 circuit 형태
