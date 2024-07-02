"""dbState models."""

from __future__ import annotations
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field
from beanie import Document, Link
from typing import List, Literal
from dataclasses import dataclass

__all__ = ("DBState", "dbInit")


class dbState(BaseModel):
    version: str
    lastUpdate: int  # timestamp(ms), UTC


TIME_SEG = Literal["DAY", "HOUR", "MIN"]
TABLES = Literal["nation"]


class DBState(Document):
    """DBState DB representation."""

    table: TABLES  # collection 담당할 내용
    time_seg: TIME_SEG  # Day, Min 단위로 저장 나누고 변화 생기면 DBState 생성
    version: str  # YYYYMMDD-24시간 기준 HHMMSS
    lastUpdate: int  # timestamp(ms), UTC

    # collections 에서 변경사항 있는 ObjectID들
    deleted: List[Link] = Field(default=[])
    added: List[Link] = Field(default=[])
    modified: List[Link] = Field(default=[])

    prev: Optional[Link[DBState]]  # 이전 기록

    @property
    def created(self) -> datetime | None:
        """Datetime car was created from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        name = "dbState"
        use_state_management = True


dbInit = (DBState,)
