from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field
from typing import Literal, List


class testReadingValue(BaseModel):
    value: float = Field(ge=0)  # 측정 불가 뜰 경우 0으로 처리
    unit: str


class FH5_test_readings(BaseModel):

    # test readings
    maxspeed: testReadingValue
    zero100: testReadingValue
    output: testReadingValue
    tork: testReadingValue
    weight: testReadingValue
    skid_pad: testReadingValue
