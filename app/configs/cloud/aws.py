from pydantic_settings import BaseSettings, SettingsConfigDict
from argparser import args

ENV_FILE = f"./envs/.{args.mode}.env"

__all__ = ("_AWS_S3_Settings",)


class _AWS_S3_Settings(BaseSettings):
    REGION: str
    BUCKET: str
    CREDENTIALS_ACCESS_KEY: str
    CREDENTIALS_SECRET_KEY: str

    ## Pydantic V2
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore", env_prefix="AWS_"
    )
