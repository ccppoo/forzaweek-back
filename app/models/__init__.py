from .car import dbInit as carDBInit
from .i18n import dbInit as i18nDBInit
from .manufacturer import dbInit as manufacturerDBInit
from .nation import dbInit as nationDBInit
from .tag import dbInit as tagDBInit
from .dbState import dbInit as dbStateDBInit
from .decal import dbInit as decalDBInit
from .track import dbInit as trackDBInit
from .tuning import dbInit as tuningDBInit
from .user import dbInit as userDBInit
from .comment import dbInit as commentDBInit
from .board import dbInit as boardDBInit
from .tagging import dbInit as taggingDBInit

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
    *tuningDBInit,
    *userDBInit,
    *commentDBInit,
    *boardDBInit,
    *taggingDBInit,
)
