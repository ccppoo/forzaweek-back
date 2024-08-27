from .i18n import dbInit as i18nDBInit
from .base import RaceRouteBase
from .race_route import RaceRoute

dbInit = (
    RaceRouteBase,
    RaceRoute,
    *i18nDBInit,
)
