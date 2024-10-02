from .base import FH5_TODO
from typing import List, Optional
from datetime import datetime


class WeeklyChallenge(FH5_TODO):
    # world: str  # mexico, rally, hot wheels
    # season_point: int
    # car_limit: Optional[CarLimit]
    # reward: Optional[Reward]

    # 이거는 챕터 1~5개 있고 시키는거 있음.
    chapter: List[str]

    class Settings:
        name = "weeklyChallenge"


class DailyChallenge(FH5_TODO):
    # 일일 첼린지
    start_date: datetime
    description: str

    class Settings:
        name = "dailyChallenge"


class EventLabTODO(FH5_TODO):
    # 이벤트 랩 한 번 하는거
    event_lab: str

    class Settings:
        name = "event_lab_TODO"


class StuntTODO(FH5_TODO):

    stunt_type: str  # speed zone, danger sign, speed trap, drift
    stunt: str  # 스턴트 ID

    class Settings:
        name = "Stunt_TODO"


class ChallengeTODO(FH5_TODO):
    # 무적 난이도 3개 중에 2개 우승

    race_routes: List[str]

    class Settings:
        name = "challenge_TODO"


class SeasonChampionship(FH5_TODO):

    race_routes: List[str]

    class Settings:
        name = "SeasonChampionship"


class MonthlyRivalTODO(FH5_TODO):

    race_route: str

    class Settings:
        name = "monthlyRival_TODO"


class TreasureHunt(FH5_TODO):

    class Settings:
        name = "treasureHunt_TODO"


class PhotoChallenge(FH5_TODO):

    description: str

    class Settings:
        name = "photoChallenge_TODO"


class HorizonOpenTODO(FH5_TODO):

    class Settings:
        name = "horizonOpen_TODO"


class HorizonTourTODO(FH5_TODO):

    class Settings:
        name = "horizonTour_TODO"
