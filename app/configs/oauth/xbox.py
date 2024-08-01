from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from argparser import args

ENV_FILE = f"./envs/.{args.mode}.env"

__all__ = ("_XBoxOAuth",)


class _XBoxOAuth(BaseSettings):
    CLIENT_ID: str | None
    CLIENT_SECRET: str | None
    REDIRECT_URI: str | None
    SCOPES: str | None
    OAUTH_ALGORITHMS: List[str] | None
    OAUTH_AUDIENCE: List[str] | None
    TOKEN_ISSUER: str | None

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        title="xbox oauth env config",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="AZURE_XBOX_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    @field_validator("OAUTH_ALGORITHMS", "OAUTH_AUDIENCE", mode="before")
    def set_algorithms(cls, v: str) -> List[str]:
        return [x for x in [v.strip() for v in v.split(",")] if x]
