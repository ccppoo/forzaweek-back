from .i18n import dbInit as i18nDBInit
from .base import CustomMapBase

dbInit = (
    CustomMapBase,
    *i18nDBInit,
)
