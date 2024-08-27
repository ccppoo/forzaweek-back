from .country import Country
from .base import CountryBase
from .i18n import dbInit as i18nDBInit

dbInit = (
    CountryBase,
    Country,
    *i18nDBInit,
)
