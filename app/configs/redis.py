from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from argparser import args

__all__ = ("_RedisSettings",)


ENV_FILE = f"./envs/.{args.mode}.env"


class _RedisSettings(BaseSettings):
    HOST: str
    HOST_PORT: int
    USERNAME: str | None
    PASSWORD: str | None
    DATABASE: str | int = 0

    ## Pydantic V2
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="REDIS_",
    )

    @property
    def URI(self) -> RedisDsn:
        _uri = "redis://"
        if self.USERNAME and self.PASSWORD:
            _uri += f"{self.USERNAME}:{self.PASSWORD}"
        if self.USERNAME and not self.PASSWORD:
            _uri += f"{self.USERNAME}"
        if self.USERNAME:
            _uri += "@"
        _uri += f"{self.HOST}:{self.HOST_PORT}/{self.DATABASE}"

        return _uri
