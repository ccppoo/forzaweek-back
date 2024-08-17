from pydantic import BaseModel, Field
from typing import Optional

__all__ = ("R2_ObjectMetaData",)


class R2_ObjectMetaData(BaseModel):
    upload_user_email: str  # public user id
    upload_user_oid: Optional[str] = Field(None)  # private user id (user doc id)
