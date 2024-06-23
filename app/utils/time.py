from datetime import datetime, timezone


def datetime_utc() -> datetime:
    return datetime(tzinfo=timezone.utc)
