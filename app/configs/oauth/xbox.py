from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from argparser import args
from pathlib import Path
import json


ENV_FILE = f"./envs/.{args.mode}.env"

__all__ = ("_XBoxOAuth",)


class MicrosoftJWTKey(BaseModel):
    kty: str
    use: str
    kid: str
    x5t: str
    n: str
    e: str
    x5c: List[str]
    issuer: str


class _XBoxOAuth(BaseSettings):
    CLIENT_ID: str | None
    CLIENT_SECRET: str | None
    REDIRECT_URI: str | None
    SCOPES: str | None
    OAUTH_ALGORITHMS: List[str] | None
    OAUTH_AUDIENCE: List[str] | None
    TOKEN_ISSUER: str | None

    TOKEN_KEY_FILE: str | None

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

    def load_jwt_keys(self) -> dict[str, MicrosoftJWTKey]:
        # load JWT keys after initiated
        # configuration, these can be seen in valid JWTs from Azure B2C
        # TODO: to frozen dict?
        # TODO: fetch JSON file every time server starts?
        KEY_FILE_DIR = "./keys"
        key_file = str(Path(KEY_FILE_DIR, self.TOKEN_KEY_FILE))
        ms_jwt_keys = dict()
        with open(key_file, mode="r", encoding="utf-8") as kf:
            keys_json = json.load(kf)
            for key in keys_json["keys"]:
                ms_JWT_key = MicrosoftJWTKey(**key)
                ms_jwt_keys[ms_JWT_key.kid] = ms_JWT_key
        return ms_jwt_keys
