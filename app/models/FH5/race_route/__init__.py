from .i18n import dbInit as i18nDBInit
from .base import RaceRouteBase
from .race_route import RaceRouteFH5

# from .hot_wheels import HotWheelsRaceRoute
# from .rally_adventure import RallyAdventureRaceRoute

__all__ = (
    "RaceRouteBase",
    "RaceRouteFH5",
    # "HotWheelsRaceRoute",
    # "RallyAdventureRaceRoute",
)

dbInit = (
    RaceRouteBase,
    RaceRouteFH5,
    # HotWheelsRaceRoute,
    # RallyAdventureRaceRoute,
    *i18nDBInit,
)
