from .base import ManufacturerBase
from .manufacturer import Manufacturer
from .i18n import dbInit as i18nDBInit
from .i18n import ManufacturerDescription, ManufacturerAlias, ManufacturerName

dbInit = (
    ManufacturerBase,
    Manufacturer,
    *i18nDBInit,
)
