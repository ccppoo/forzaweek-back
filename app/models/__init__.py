from .car import dbInit as carDBInit
from .i18n import dbInit as i18nDBInit
from .manufacturer import dbInit as manufacturerDBInit
from .nation import dbInit as nationDBInit
from .stat import dbInit as statDBInit
from .tag import dbInit as tagDBInit
from .decal import dbInit as decalDBInit
from .tuning import dbInit as tuningDBInit
from .track import dbInit as trackDBInit
from .tuning import dbInit as tuningDBInit
from .bodyStyle import dbInit as bodyStyleDBInit
from .driveTrain import dbInit as driveTrainDBInit
from .engine import dbInit as engineDBInit

__all__ = ["models"]


models = [
    *i18nDBInit,
    *nationDBInit,
    *manufacturerDBInit,
    *bodyStyleDBInit,
    *driveTrainDBInit,
    *engineDBInit,
    *carDBInit,
    *statDBInit,
    *tagDBInit,
    *decalDBInit,
    *tuningDBInit,
    *trackDBInit,
    *tuningDBInit,
]
