from app.models.base import DocumentBase

from pydantic import BaseModel, Field

__all__ = ("ManufacturerBase",)


class ManufacturerBase(DocumentBase):

    class Settings:
        name = "ManufacturerBase"
