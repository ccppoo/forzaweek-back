from app.models.base import DocumentBase


from pydantic import BaseModel, Field

__all__ = ("CarBase",)


class CarBase(DocumentBase):

    class Settings:
        name = "CarBase"
        is_root = True
