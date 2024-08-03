from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from argparser import args

__all__ = ("_SecuritySettings",)

ENV_FILE = f"./envs/.{args.mode}.env"


class _SecuritySettings(BaseSettings):
    TOKEN_SECRET: str = Field(min_length=5)
    TOKEN_LIFETIME: int = Field(gt=600)
    RESET_SECRET: str = Field(min_length=5)
    RESET_LIFETIME: int = Field(gt=300)
    UID_GEN_SALT: str
    UID_GEN_SALT_PUBLIC: str

    ## Pydantic V2
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="SECURITY_",
    )
