from datetime import datetime, timezone, UTC
from enum import Enum


class Datetime_Format(str, Enum):
    YYYYMMDD = "%Y%m%d"
    HHMMSS = "%H%M%S"


def datetime_utc() -> datetime:
    return datetime.now(UTC)


def timestamp_utc_s() -> int:
    # return timestamp as seconds
    return int(datetime.now(tz=timezone.utc).timestamp())


def timestamp_utc_ms() -> int:
    # return timestamp as milliseconds
    return int(datetime.now(tz=timezone.utc).timestamp() * 1000)


def datetime_utc_format(format: Datetime_Format) -> str:
    return datetime.now(tz=timezone.utc).strftime(format)
