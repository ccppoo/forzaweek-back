"""Car models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from typing import Literal
import pymongo

__all__ = ("FrozaUser",)


class FrozaUser(Document):
    """FrozaUser DB representation."""

    name: str
    version: str

    @property
    def created(self) -> datetime | None:
        """Datetime car was created from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        name = "forzaUsers"
