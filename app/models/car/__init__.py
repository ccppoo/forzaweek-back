from .base import CarBase
from .original import Car
from .i18n import dbInit as i18nDBInit
from .i18n import CarAlias, CarName

dbInit = (
    CarBase,
    Car,
    *i18nDBInit,
)
