from pydantic import BaseModel, Field


class XboxUserInfo(BaseModel):
    gamer_tag: str = Field(description="gamer tags displayed in xbox page and in game")
    user_hash: str = Field(description="xbox user hash")
    xuid: str = Field(description="xbox user id")
    profile_image: str = Field(description="xbox user profile image URL")
    preferred_color: str = Field(
        description="xbox user preferred color URL (JSON file)"
    )
