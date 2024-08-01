from pydantic import Field, RedisDsn, BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from argparser import args
import urllib.parse

__all__ = (
    "runtimeSettings",
    "dbSettings",
    "securitySettings",
    "redisSettings",
    "oauthSettings",
    "awsSettings",
)

ENV_FILE = f"./envs/.{args.mode}.env"
ENV_FILE = f"./envs/.dev.env"


class _RuntimeSettings(BaseSettings):
    TEMPFILE_BASE_DIR: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="SYSTEM_",
    )


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


class _AWS_S3_Settings(BaseSettings):
    REGION: str
    BUCKET: str
    CREDENTIALS_ACCESS_KEY: str
    CREDENTIALS_SECRET_KEY: str

    ## Pydantic V2
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore", env_prefix="AWS_"
    )


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
            return f"mongodb://{_username}@{dbSettings.HOST}:{dbSettings.HOST_PORT}"
        else:
            # return f"mongodb://{_username}:{_password}@{dbSettings.HOST}:{dbSettings.HOST_PORT}/{self.DATABASE}"
            return f"mongodb://{_username}:{_password}@{dbSettings.HOST}:{dbSettings.HOST_PORT}"


class _SecuritySettings(BaseSettings):
    TOKEN_SECRET: str = Field(min_length=5)
    TOKEN_LIFETIME: int = Field(gt=600)
    RESET_SECRET: str = Field(min_length=5)
    RESET_LIFETIME: int = Field(gt=300)
    UID_GEN_SALT: str

    ## Pydantic V2
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="SECURITY_",
    )


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
        if self.USERNAME and self.PW:
            _uri += f"{self.USERNAME}:{self.PW}"
        if self.USERNAME and not self.PW:
            _uri += f"{self.USERNAME}"
        if self.USERNAME:
            _uri += "@"
        _uri += f"{self.HOST}:{self.HOST_PORT}/{self.DATABASE}"

        return _uri


class XBoxOAuth(BaseSettings):
    CLIENT_ID: str | None
    CLIENT_SECRET: str | None
    REDIRECT_URI: str | None
    SCOPES: str | None
    OAUTH_ALGORITHMS: List[str] | None
    OAUTH_AUDIENCE: List[str] | None
    TOKEN_ISSUER: str | None

    model_config = SettingsConfigDict(
        title="xbox oauth env config",
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="AZURE_XBOX_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    @field_validator("OAUTH_ALGORITHMS", "OAUTH_AUDIENCE", mode="before")
    def set_algorithms(cls, v: str) -> List[str]:
        return [x for x in [v.strip() for v in v.split(",")] if x]


class _OAuthSettings(BaseSettings):
    xbox: XBoxOAuth = Field(default_factory=XBoxOAuth)


dbSettings = _DatabaseSettings()
securitySettings = _SecuritySettings()
redisSettings = _RedisSettings()
oauthSettings = _OAuthSettings()
awsSettings = _AWS_S3_Settings()

runtimeSettings = _RuntimeSettings()
cfSettings = _CF_R2_Settings()
