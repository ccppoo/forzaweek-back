from datetime import datetime
from typing import Any, List
from beanie import Document, Link
from pydantic import BaseModel, Field
from app.models.i18n import i18n
from app.types.http import Url

__all__ = ("Vote",)


class Vote(BaseModel):
    # 사용자 ID
    up: List[str] = Field(default=[])
    down: List[str] = Field(default=[])
