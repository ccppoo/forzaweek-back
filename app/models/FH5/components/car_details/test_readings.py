from pydantic import BaseModel, Field

__all__ = ("TestReadings",)


class testReadingValue(BaseModel):
    value: float = Field(ge=0)  # 측정 불가 뜰 경우 0으로 처리
    unit: str


class TestReadings(BaseModel):

    maxspeed: testReadingValue
    zero100: testReadingValue
    output: testReadingValue
    torque: testReadingValue
    weight: testReadingValue
    skid_pad: testReadingValue
