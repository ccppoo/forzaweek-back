from pydantic_settings import BaseSettings, SettingsConfigDict
from argparser import args

__all__ = ("_RuntimeSettings",)

ENV_FILE = f"./envs/.{args.mode}.env"


class _RuntimeSettings(BaseSettings):
    TEMPFILE_BASE_DIR: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="SYSTEM_",
    )
