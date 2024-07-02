from pydantic import BaseModel, Field

from .major_parts import FH5_major_parts as Major_Parts
from .meta import FH5_meta as Meta
from .performance import FH5_performance as Performance
from .test_readings import FH5_test_readings as Test_Readings


class CarFH5base(BaseModel):
    meta: Meta  # IndexedDB 따로 생성
    performance: Performance  # IndexedDB 따로 생성 + PI랑 같이
    pi: int = Field(ge=100, le=999)


__all__ = (
    "Major_Parts",
    "Meta",
    "Performance",
    "Test_Readings",
    "CarFH5base",
)
