from pydantic import BaseModel, Field
from typing import List, Optional


class CarLimit(BaseModel):
    carFH5: Optional[str]  # 자동차 하나
    origin: List[str]  # 나라
    PI: int  # B, A, S1 클래스
    division: List[str]
    manufacturer: List[str]
