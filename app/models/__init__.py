from .car import dbInit as carDBInit
from .i18n import dbInit as i18nDBInit
from .manufacturer import dbInit as manufacturerDBInit
from .nation import dbInit as nationDBInit
from .tag import dbInit as tagDBInit
from .dbState import dbInit as dbStateDBInit
from .decal import dbInit as decalDBInit
from .track import dbInit as trackDBInit

__all__ = ["models"]

models = (
    *dbStateDBInit,
    *i18nDBInit,
    *nationDBInit,
    *manufacturerDBInit,
    *carDBInit,
    *tagDBInit,
    *decalDBInit,
    *trackDBInit,
)
