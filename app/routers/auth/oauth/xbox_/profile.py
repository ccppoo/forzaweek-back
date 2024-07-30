from __future__ import annotations
from pydantic import BaseModel, Field
from xbox.webapi.api.provider.profile import ProfileResponse, ProfileSettings
from xbox.webapi.api.provider.profile.models import ProfileUser, Setting


class XboxProfilePreferredColor(BaseModel):

    primaryColor: str = Field(default="107c10")
    secondaryColor: str = Field(default="102b14")
    tertiaryColor: str = Field(default="155715")


class XboxProfile(BaseModel):

    id: str
    host_id: str

    Gamertag: str = Field(default="")
    ModernGamertag: str = Field(default="")
    RealNameOverride: str = Field(default="")
    UniqueModernGamertag: str = Field(default="")
    RealNameOverride: str = Field(default="")
    GameDisplayPicRaw: str = Field(default="")
    PreferredColor: str = Field(default="")  # Url -> JSON으로 저장

    @staticmethod
    def fromProfileUser(profileUser: ProfileUser) -> XboxProfile:

        _id = profileUser.model_dump(include=["id", "host_id"])

        settings = {}
        for setting in profileUser.settings:
            if _s := XboxProfile._parseSetting(setting):
                settings.update(_s)
        return XboxProfile(**_id, **settings)

    @staticmethod
    def _parseSetting(setting: Setting):
        _settings = (
            "Gamertag",
            "ModernGamertag",
            "RealNameOverride",
            "UniqueModernGamertag",
            "RealNameOverride",
            "GameDisplayPicRaw",
            "PreferredColor",
        )
        if setting.id in _settings:
            return {setting.id: setting.value}
        return
