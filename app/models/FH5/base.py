from app.models.base import DocumentBase

__all__ = ("FH5DocumentBase",)


class FH5DocumentBase(DocumentBase):

    class Settings:
        name = "FH5"
