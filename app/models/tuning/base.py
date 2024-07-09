from datetime import datetime
from beanie import Document, Link
from pydantic import Field
from typing import List
from app.models.tag import Tag
from app.models.car import Car

__all__ = ("TuningBase",)


class TuningBase(Document):
    """Tuning 작성할 때 FH5, FH4 모두 이거 상속 받기"""

    # id

    share_code: str  # 공유코드 숫자 9자리
    car: Link[Car]
    creator: str

    tags: List[Link[Tag]] = Field(default=[])

    @property
    def created(self) -> datetime | None:
        """Datetime tuning was created from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        name = "tuning"
        use_state_management = True
        is_root = True
