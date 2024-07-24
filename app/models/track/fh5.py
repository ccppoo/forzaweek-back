from app.models.track.base import TrackBase
from app.models.track.traits.fh5 import TrackCategory, TrackFormat, TrackFullPathImage
from app.models.base import GameBase
from app.models.track.fh5 import TrackBase
from app.types import GAME
from app.types.http import Url
from typing import List, Optional
from pydantic import Field

__all__ = ("Track_FH5",)


class Track_FH5(GameBase, TrackBase, TrackFullPathImage, TrackCategory, TrackFormat):
    """
    FH5 공식 트랙 - 멕시코+DLC(랠리, 핫휠) 이름, 종류, 카테고리 기본적인 정보만 저장하는 DB

    # TODO: Map 위치 - 트랙 사진(구글맵처럼) 추가
    # TODO: 트랙 사진
    """

    game: GAME = "FH5"
    # name
    # liberal_translation
    # tags
    # world

    # fullPathImage
    # imageURLs
    # firstImage
    # category
    # format
    # laps

    imageURLs: List[Url] = Field(default=[])
    firstImage: Optional[Url] = Field(default=None)

    def to_front_read(self):

        _partial = self.model_dump(
            include=[
                "format",
                "laps",
                "category",
                "fullPathImage",
                "id",
                "name_en",
                "world",
                "game",
            ]
        )

        name = [x.model_dump(include=["value", "lang"]) for x in self.name]
        liberal_translation = [
            x.model_dump(include=["value", "lang"]) for x in self.liberal_translation
        ]
        _tags = [t.to_simple() for t in self.tag]

        return {
            **_partial,
            "tag": _tags,
            "liberal_translation": liberal_translation,
            "name": name,
        }

    def to_front_read2(self):
        _partial = self.model_dump(
            include=[
                "format",
                "laps",
                "category",
                "fullPathImage",
                "id",
                "name_en",
                "world",
                "game",
            ]
        )
        _tags = [t.to_simple() for t in self.tag]

        name = {x.lang: x.value for x in self.name}
        liberal_translation = {x.lang: x.value for x in self.liberal_translation}
        return {
            **_partial,
            "tag": _tags,
            "liberal_translation": liberal_translation,
            "name": name,
        }

    def to_indexedDB(self):

        name = {x.lang: x.value for x in self.name}
        liberal_translation = None
        if self.liberal_translation:
            liberal_translation = {x.lang: x.value for x in self.liberal_translation}
        return {
            "id": str(self.id),
            "game": self.game,
            "category": self.category,
            "format": self.format,
            "laps": self.laps,
            "world": self.world,
            "name": name,
            "liberal_translation": liberal_translation,
        }

    def to_indexedDB_image(self):
        # &id
        return {
            "id": str(self.id),
            "first": self.firstImage,
            "images": self.imageURLs,
            "fullPathImage": {
                "zoom_out": self.fullPathImage.zoom_in,
                "zoom_in": self.fullPathImage.zoom_out,
            },
        }

        pass

    class Settings:
        name = "track_FH5"
        use_state_management = True


dbInit = (Track_FH5,)
