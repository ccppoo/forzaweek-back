from pydantic import BaseModel, Field


class MircrosoftUserInfo(BaseModel):

    uid: str = Field(description="Microsoft user id")
    email: str = Field(description="Microsoft log in email")
