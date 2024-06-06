"""Nation models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr, Field
from typing import Literal, List
import pymongo
from .i18n import i18n


__all__ = ("Nation", "dbInit")


class NationName(i18n):
    # value : str
    # lang: str
    pass


class Nation(Document):
    """Nation DB representation."""

    name: List[Link[NationName]]

    @property
    def created(self) -> datetime | None:
        """Datetime car was created from ID."""
        return self.id.generation_time if self.id else None

    def to_json(self, lang: Optional[str]) -> dict[str, Any]:
        if lang:
            for nationName in self.name:
                if nationName.lang == lang:
                    return nationName.model_dump(exclude=["id", "revision_id"])
        data = []
        for nationName in self.name:
            nationName: NationName
            data.append(nationName.model_dump(exclude=["id", "revision_id"]))
        return data

    class Settings:
        name = "nation"


dbInit = (Nation, NationName)
