from pydantic import BaseModel, Field
from typing import Optional, Literal

__all__ = ("RacingFormat",)


class RacingFormat(BaseModel):
    """
    sprint, trail, course, circuit, scramble 지칭하는 것들
    """

    format_name: Literal["sprint", "trail", "course", "circuit", "scramble"]
    format_topology: Literal[
        "linear", "circular"
    ]  # 이름 다르지만, N바퀴 도는거랑, 출발->목적지 도착하는 형태 구분
    laps: Optional[int] = Field(ge=0)
