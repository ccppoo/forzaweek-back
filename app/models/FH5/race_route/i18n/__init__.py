from .name import RaceRouteName, RaceRouteNameTranslated
from .description import RaceRouteDescription

__all__ = (
    "RaceRouteName",
    "RaceRouteDescription",
    "RaceRouteNameTranslated",
)

dbInit = (
    RaceRouteName,
    RaceRouteNameTranslated,
    RaceRouteDescription,
)
