from pydantic_settings import BaseSettings, SettingsConfigDict
from argparser import args

__all__ = ("_CF_R2_Settings",)

ENV_FILE = f"./envs/.{args.mode}.env"


class _CF_R2_Settings(BaseSettings):

    ACCESS_KEY: str
    SECRET_ACCESS_KEY: str
    TOKEN: str
    R2_ENDPOINT: str
    LOCATION: str
    BUCKET: str
    URL_BASE: str

    ## Pydantic V2
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore", env_prefix="CF_"
    )
