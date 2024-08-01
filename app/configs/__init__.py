from argparser import args
from .runtime import _RuntimeSettings
from .redis import _RedisSettings
from .security import _SecuritySettings
from .db import _DatabaseSettings
from .cloud import *
from .oauth import *

__all__ = (
    "runtimeSettings",
    "redisSettings",
    "securitySettings",
    "dbSettings",
    "oauthSettings",
    "awsSettings",
    "cfSettings",
)

ENV_FILE = f"./envs/.{args.mode}.env"

runtimeSettings = _RuntimeSettings()
redisSettings = _RedisSettings()
securitySettings = _SecuritySettings()
dbSettings = _DatabaseSettings()


oauthSettings = _OAuthSettings()
awsSettings = _AWS_S3_Settings()

cfSettings = _CF_R2_Settings()
