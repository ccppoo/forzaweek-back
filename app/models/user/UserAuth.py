from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal, Annotated
from app.utils.time import datetime_utc
from app.utils.hash import user_uuid
from app.models.user.sso.microsoft import MircrosoftUserInfo, XboxUserInfo
from beanie import Document, Link, Indexed
import pymongo


class OAuthSolutions(BaseModel):

    microsoft: Optional[MircrosoftUserInfo] = Field(default=None)
    xbox: Optional[XboxUserInfo] = Field(default=None)


OAUTH_PROVIDERS = [
    "MS",
]


class UserAuth(Document):

    # id uuid5()
    user_id: Annotated[str, Indexed(index_type=pymongo.TEXT)] = Field(
        description="uuid5 hashed user id"
    )

    # 사용자 행동 -> Reputations, 등등

    # oauth
    oauth: OAuthSolutions

    # meta
    created_at: datetime = Field(default_factory=datetime_utc)
    recent_update: datetime = Field(default_factory=datetime_utc)
    last_login: datetime = Field(default_factory=datetime_utc)

    @staticmethod
    async def find_oauth_MS(
        *,
        uid: str,
        email: str,
    ) -> UserAuth | None:
        user = await UserAuth.find_one(
            UserAuth.oauth.microsoft.email == email, UserAuth.oauth.microsoft.uid == uid
        )
        return user

    class Settings:
        name = "user"
        use_state_management = True
