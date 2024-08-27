from typing import Literal
from pydantic import BaseModel

FH5_WORLD = ["Mexico", "Hot Wheels", "Rally"]


class WorldDependent(BaseModel):
    world: Literal["Mexico", "Hot Wheels", "Rally"]  # DLC 지역과 기본 지역 구분
