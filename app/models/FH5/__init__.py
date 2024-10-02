from .base import FH5DocumentBase

from .car import dbInit as carDBInit
from .custom_map import dbInit as customMapDBInit
from .decal import dbInit as decalDBInit
from .race_route import dbInit as raceRouteDBInit
from .tuning import dbInit as tuningDBInit
from .vynil_groups import dbInit as VGDBInit
from .festival import dbInit as festivalDBInit

dbInit = (
    FH5DocumentBase,
    *carDBInit,
    *customMapDBInit,
    *decalDBInit,
    *raceRouteDBInit,
    *tuningDBInit,
    *VGDBInit,
    *festivalDBInit,
)
