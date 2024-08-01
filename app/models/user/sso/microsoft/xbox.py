from pydantic import BaseModel, Field


class XboxUserInfo(BaseModel):
    gamer_tag: str = Field(description="gamer tags displayed in xbox page and in game")
    user_hash: str = Field(description="xbox user hash")
    xuid: str = Field(description="xbox user id")
