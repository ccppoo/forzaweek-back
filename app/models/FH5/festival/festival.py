from __future__ import annotations

from ..base import FH5DocumentBase
from pydantic.alias_generators import to_snake
from pprint import pprint
from pydantic import BaseModel, Field
from beanie import Link
from app.types.http import Url
from typing import List, Optional
from datetime import datetime
from .reward import Reward
from .todo import FH5_TODO
from .todo import WeeklyChallenge, DailyChallenge, MonthlyRivalTODO


class Festival(FH5DocumentBase):

    start_date: datetime
    end_date: datetime

    name: str
    number: int

    rewards: List[Reward]

    # monthly challenge - 주마다 하는거 상관없는 할 것들
    monthly_rivals: List[Link[MonthlyRivalTODO]]

    # 여름 가을 겨울 봄 4개
    series: List[Link[FestivalSeries]]

    # relation
    prev: Optional[Link[Festival]]
    next: Optional[Link[Festival]]

    async def as_json(self):
        return

    class Settings:
        name = "FH5_Festival"
        is_root = True


class FestivalSeries(FH5DocumentBase):

    # 하나의 Week마다 해야할 것들
    start_date: datetime
    end_date: datetime

    season: str  # 여름/가을/겨울/봄

    rewards: List[Reward]  # 시리즈 전체 보상

    # 이것들은 월드 상관없이 할 수 있는 것들
    weekly_challenge: Optional[Link[WeeklyChallenge]]
    daily_challenge: List[Link[DailyChallenge]]

    # 월드에 종속되어 있는 것들
    mexico: List[Link[FH5_TODO]]
    rally: List[Link[FH5_TODO]]
    hotwheels: List[Link[FH5_TODO]]

    # relation
    prev: Optional[Link[FestivalSeries]]
    next: Optional[Link[FestivalSeries]]

    async def as_json(self):
        return

    class Settings:
        name = "FH5_FestivalSeries"
        is_root = True
