from pydantic import Field, BaseModel
from pprint import pprint

__all__ = ("HasUploader",)


class HasUploader(BaseModel):

    uploader: str  # user_id (oid)
