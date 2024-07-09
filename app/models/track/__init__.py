from .base import dbInit as TrackBasedbInit
from .fh5 import dbInit as TrackdbInit_FH5

__all__ = ("dbInit",)


dbInit = (*TrackBasedbInit, *TrackdbInit_FH5)
