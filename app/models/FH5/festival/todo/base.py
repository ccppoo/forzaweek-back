from __future__ import annotations
from app.models.FH5.base import FH5DocumentBase

from beanie import Link
from typing import List, Optional
from ..reward import Reward
from ..car_limit import CarLimit


class FH5_TODO(FH5DocumentBase):
    world: Optional[str]  # mexico, rally, hot wheels
    season_point: int
    car_limit: Optional[CarLimit]
    reward: Optional[Reward]

    class Settings:
        name = "FH5_TODO"
        is_root = True
