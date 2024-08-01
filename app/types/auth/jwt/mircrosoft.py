from pydantic import Field
from .base import JWTPayload, JWTHeader

__all__ = (
    "MicrosoftJWTHeader",
    "MicrosoftJWTPayload",
)


class MicrosoftJWTHeader(JWTHeader):
    pass


class MicrosoftJWTPayload(JWTPayload):
    ver: str = Field(description="token version")
    email: str = Field(description="subject's email")
    tid: str = Field(description="ID of the tenant that issued the token")
    aio: str = Field(description="MS internal token identifier")

    # tid == 9188040d-6c67-4c5b-b112-36a304b66dad (should be)
    # iss == https://login.live.com (should be)

    @property
    def uid(self):
        return self.sub

    @property
    def azure_client_id(self):
        return self.aud
