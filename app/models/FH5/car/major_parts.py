from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field
from typing import Literal, List


DRIVING_SYSTEM = Literal["AWD", "FWD", "RWD"]


class FH5_major_parts(BaseModel):

    # 주요 부품 - 타이어, 서스펜션,
    # TODO: 나중에 다 Literal로 바꿔서 한정시키기
    tier: str
    suspension: str
    drivingSystem: DRIVING_SYSTEM
