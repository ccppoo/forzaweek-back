from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import List, Optional

__all__ = ("i18n", "dbInit")

ISO_639 = ["en", "ko"]


class i18n(Document):
    value: str
    lang: str
    country: Optional[str] = Field(None)  # 국가세부

    class Settings:
        is_root = True


dbInit = [i18n]
