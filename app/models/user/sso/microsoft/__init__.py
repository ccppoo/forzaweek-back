from pydantic import BaseModel
from .microsoft import MircrosoftUserInfo
from .xbox import XboxUserInfo

__all__ = (
    "MircrosoftUserInfo",
    "XboxUserInfo",
)
