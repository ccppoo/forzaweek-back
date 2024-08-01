from pydantic import Field
from pydantic_settings import BaseSettings
from .xbox import _XBoxOAuth


__all__ = ("_OAuthSettings",)


class _OAuthSettings(BaseSettings):
    xbox: _XBoxOAuth = Field(default_factory=_XBoxOAuth)
