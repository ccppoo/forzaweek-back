from app.models.track.base import TrackBase
from app.models.track.traits.fh5 import RaceCategory, RacingFormat

__all__ = ("Track_FH5",)


class Track_FH5(TrackBase, RaceCategory, RacingFormat):
    """
    FH5 공식 트랙 - 멕시코+DLC(랠리, 핫휠) 이름, 종류, 카테고리 기본적인 정보만 저장하는 DB

    # TODO: Map 위치 - 트랙 사진(구글맵처럼) 추가
    # TODO: 트랙 사진
    """

    # name
    # tag
    # world

    # category_name
    # format_name
    # format_topology
    # laps

    class Settings:
        name = "track_FH5"
        use_state_management = True


dbInit = (Track_FH5,)
