from .i18n import dbInit as i18nDBInit
from .manufacturer import dbInit as manufacturerDBInit
from .tag import dbInit as tagDBInit
from .dbState import dbInit as dbStateDBInit

from .user import dbInit as userDBInit
from .comment import dbInit as commentDBInit
from .board import dbInit as boardDBInit
from .FH5 import dbInit as FH5DBInit
from .country import dbInit as countryDBInit
from .car import dbInit as carBaseDBInit

__all__ = ["models"]

models = (
    *countryDBInit,
    *i18nDBInit,
    *carBaseDBInit,
    *dbStateDBInit,
    *manufacturerDBInit,
    *tagDBInit,
    *userDBInit,
    *commentDBInit,
    *boardDBInit,
    *FH5DBInit,
)
