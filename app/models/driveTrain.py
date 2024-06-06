"""Nation models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr, Field
from typing import Literal, List
import pymongo
from .i18n import i18n


__all__ = ("DriveTrain", "dbInit")


class DriveTrainName(i18n):
    # value : str
    # lang: str
    pass


class DriveTrainDescription(i18n):
    pass


class DriveTrain(Document):
    """DriveTrain DB representation."""

    abbreviation: str  # 공통 영어
    name: List[Link[DriveTrainName]]
    description: List[Link[DriveTrainDescription]]

    @property
    def created(self) -> datetime | None:
        """Datetime car was created from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        name = "driveTrain"


dbInit = (DriveTrain, DriveTrainName, DriveTrainDescription)
