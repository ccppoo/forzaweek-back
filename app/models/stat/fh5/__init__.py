from pydantic import BaseModel, Field

from .detailed_tuning import DetailedTunings
from .major_parts import MajorParts
from .meta import Meta
from .performance import Performance
from .test_readings import TestReadings
from .PI import PI

__all__ = (
    "DetailedTunings",
    "MajorParts",
    "Meta",
    "Performance",
    "TestReadings",
    "CarBaseStat_FH5",
    "PI",
    "TuningStat_FH5",
)


class CarBaseStat_FH5(PI):
    """FH5 자동차 기본 정보에 들어있는 성능 수치"""

    meta: Meta  # IndexedDB 따로 생성
    performance: Performance  # IndexedDB 따로 생성 + PI랑 같이


class TuningStat_FH5(PI):
    """FH5 튜닝 정보에 사용할 것

    front form과 동일하게 유지할 것
    """

    detailedTuning: DetailedTunings
    performance: Performance
    testReadings: TestReadings
    tuningMajorParts: MajorParts
