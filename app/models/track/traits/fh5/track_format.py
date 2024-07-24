from pydantic import BaseModel, Field
from typing import Optional, Literal

__all__ = ("RacingFormat",)


class TrackFormat(BaseModel):
    """
    sprint, trail, course, circuit, scramble 지칭하는 것들
    """

    format: Literal[
        "sprint",
        "trail",
        "course",
        "circuit",
        "scramble",
        "street",
        "crossCountry",
        "crossCountryCircuit",
    ]
    laps: Optional[int] = Field(ge=0)  # 0이면 sprint 형태, 1이상이면 circuit 형태
