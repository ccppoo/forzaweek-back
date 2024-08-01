from pydantic_settings import BaseSettings, SettingsConfigDict
import urllib.parse
from argparser import args

__all__ = ("_DatabaseSettings",)


ENV_FILE = f"./envs/.{args.mode}.env"


class _DatabaseSettings(BaseSettings):
    HOST: str
    HOST_PORT: int
    DATABASE: str
    USERNAME: str | None
    PASSWORD: str | None

    ## Pydantic V2
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore", env_prefix="DB_"
    )

    @property
    def URL(self) -> str:
        if not (self.USERNAME or self.PASSWORD):
            return f"mongodb://{self.HOST}:{self.HOST_PORT}"
        _username = urllib.parse.quote_plus(self.USERNAME)
        _password = urllib.parse.quote_plus(self.PASSWORD)
        if not self.PASSWORD:
            # return f"mongodb://{_username}@{dbSettings.HOST}:{dbSettings.HOST_PORT}/{self.DATABASE}"
            return f"mongodb://{_username}@{self.HOST}:{self.HOST_PORT}"
        else:
            # return f"mongodb://{_username}:{_password}@{dbSettings.HOST}:{dbSettings.HOST_PORT}/{self.DATABASE}"
            return f"mongodb://{_username}:{_password}@{self.HOST}:{self.HOST_PORT}"
