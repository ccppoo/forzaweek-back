from __future__ import annotations
from datetime import datetime
from typing import Any, List, Optional
from beanie import Document, Link
from pydantic import BaseModel, Field
from app.models.i18n import i18n
from app.types.http import Url
from app.models.components import Vote
from app.utils.time import datetime_utc
from app.models.user import UserAuth

__all__ = ("Votable",)


class Votable(BaseModel):
    # 사용자 ID
    up_voters: List[Link[UserAuth]] = Field(default=[])
    down_voters: List[Link[UserAuth]] = Field(default=[])

    async def up_vote(self, by: str):
        # down voter에 있을 경우 제거
        # by - user ID
        assert NotImplementedError("Votable::up_vote not implemented")

    async def cancel_vote(self, by: str):
        pass
        assert NotImplementedError("Votable::cancel_vote not implemented")

    async def down_vote(self, by: str):
        # up voter에 있을 경우 제거
        # by - user ID
        assert NotImplementedError("Votable::down_vote not implemented")
