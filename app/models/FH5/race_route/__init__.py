from .i18n import dbInit as i18nDBInit
from .base import RaceRouteBase

dbInit = (
    RaceRouteBase,
    *i18nDBInit,
)
