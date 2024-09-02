from app.models.base import DocumentBase

from pydantic import BaseModel, Field

__all__ = ("ManufacturerBase",)


class ManufacturerBase(DocumentBase):

    @property
    def id_str(self) -> str:
        return str(self.id)

    class Settings:
        name = "ManufacturerBase"
