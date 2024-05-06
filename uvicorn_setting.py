from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

__all__ = ("UvicornSettings",)


class UvicornSettings(BaseSettings):
    host: str
    port: int

    # Reload - DEV
    reload: bool = False
    reload_dirs: List[str] = ["./app"]
    reload_includes: List[str] = ["*.py"]
    reload_delay: float = 0.5

    # WebSocket
    # ws: str = "wsproto"
    ws_max_size: int = 16777216
    ws_ping_interval: float = 20
    ws_ping_timeout: float = 5
    ws_per_message_deflate: bool = True

    # Logging
    log_level: str | int | None = "info"
    access_log: bool = True

    # HTTP
    http: str = "httptools"
    server_header: bool = False
    date_header: bool = True
    proxy_headers: bool = True
    forwarded_allow_ips: List[str] | str | None = "*"  # Public하게 베포하게 될 경우

    # Interface
    # interface: str = "asgi3"
    interface: str = "auto"
    lifespan: str = "auto"

    # Production
    workers: int = 1

    # Resource
    limit_concurrency: int | None = None
    limit_max_requests: int | None = None
    backlog: int = 2048

    # Timeout
    timeout_keep_alive: int = 5
    timeout_graceful_shutdown: int = 5

    # Pydantic v2
    model_config = SettingsConfigDict(case_sensitive=False)
