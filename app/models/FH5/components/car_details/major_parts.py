from pydantic import BaseModel, Field
from typing import Literal

__all__ = ("MajorParts",)

# TODO: 상수들 다른 파일로 관리하기
DRIVING_SYSTEM = Literal["AWD", "FWD", "RWD"]


class MajorParts(BaseModel):

    # 주요 부품 - 타이어, 서스펜션,
    # TODO: 나중에 다 Literal로 바꿔서 한정시키기
    tire: str
    suspension: str
    drivingSystem: DRIVING_SYSTEM
