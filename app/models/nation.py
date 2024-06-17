"""Nation models."""

from datetime import datetime
from typing import Any, Optional

from beanie import Document, Indexed, Link
from typing import List
from .i18n import i18n
from app.types.http import Url

__all__ = ("Nation", "dbInit")


class NationName(i18n):
    # value : str
    # lang: str
    def to_front(self):
        return {"value": self.value, "lang": self.lang}


class Nation(Document):
    """Nation DB representation."""

    name: List[Link[NationName]]
    name_en: str
    imageURL: Url

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

    def to_json_all_lang(self, _id: bool = False) -> dict[str, Any]:
        i18ns = [x.to_front() for x in self.name]
        # 직접 id 가져오는 방법?
        _id = self.model_dump(include=["id"])["id"]

        if _id:

            return {
                "id": _id,
                "i18n": i18ns,
                "name_en": self.name_en,
                "imageURL": self.imageURL,
            }
        return {
            "i18n": i18ns,
            "name_en": self.name_en,
            "imageURL": self.imageURL,
        }

    class Settings:
        name = "nation"
        use_state_management = True


dbInit = (Nation, NationName)
