from datetime import datetime
from typing import List, Any, Optional
from beanie import Document, Link
from app.models.i18n import i18n
from app.types.http import Url
from .i18n import CountryName
from pydantic import Field
from app.models.base import DocumentBase

__all__ = ("CountryBase",)


class CountryBase(DocumentBase):
    """Country DB representation."""

    class Settings:
        name = "Country"
