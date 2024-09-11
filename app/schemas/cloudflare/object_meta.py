from pydantic import BaseModel, Field
from typing import Optional

__all__ = ("R2_ObjectMetaData",)


class R2_ObjectMetaData(BaseModel):
    email: str
    sub: str
    # user_email: str  # public user id
    # user_oid: Optional[str] = Field(None)  # private user id (user doc id)
    # user_sub: str
