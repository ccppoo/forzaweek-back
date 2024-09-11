from datetime import datetime
from typing import List, Optional, Union
from beanie import Document, Link
from pydantic import Field
from app.utils.time import datetime_utc
from pprint import pprint

from beanie.odm.actions import after_event
from beanie.odm.actions import Insert, Save, Replace, Update, SaveChanges

__all__ = ("DocumentBase",)


class DocumentBase(Document):
    """DocumentBase"""

    uploaded_at: datetime = Field(default_factory=datetime_utc)
    last_edited: Optional[datetime] = Field(default=None)

    @property
    def id_str(self) -> str:
        return str(self.id)

    @after_event(Replace, Update, SaveChanges)
    def update_last_edit(self):
        self.last_edited = datetime_utc()

    class Settings:
        pass
