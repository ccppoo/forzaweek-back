"""Manufacturer models."""

from app.models.i18n import i18n

__all__ = ("ManufacturerName", "ManufacturerAlias", "ManufacturerDescription")


class ManufacturerName(i18n):
    # value : str
    # lang: str
    pass


class ManufacturerAlias(i18n):
    # value : str
    # lang: str
    pass


class ManufacturerDescription(i18n):
    # value : str
    # lang: str
    pass
