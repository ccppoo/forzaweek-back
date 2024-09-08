from .base import RaceRouteBase


from beanie import Link
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Any, Literal
from app.models.FH5.components.race_route import TrackFormat
from app.models.i18n import i18n as I18N


FH5_RACE_FORMAT = Literal[
    "sprint",
    "trail",
    "course",
    "circuit",
    "scramble",
    "street",
    "crosscountry",
    "showcase",
    "drag",
]
FH5_TRACK_CATEGORY = Literal[
    "crosscountry", "rally", "offroad", "road", "street", "drag", "hazard", "speed"
]


class RaceRouteFH5(RaceRouteBase):

    # image_urls: List[Url] = Field(default=[])
    # first_image: Optional[Url] = Field(default=None)

    # full_path_image: FullPathImage
    # coordinate_images: List[CoordinateImage] = Field([])
    # icon_url : Url

    # name: List[Link[RaceRouteName]] = Field([])
    # name_translated: List[Link[RaceRouteNameTranslated]] = Field([])
    # description: List[Link[RaceRouteDescription]] = Field([])

    world: Literal["mexico", "hot_wheels", "rally", "event_island"]
    laps: int = Field(ge=0)
    category: FH5_TRACK_CATEGORY  # 보고 바로 직관적으로 알 수 있는 것들
    race_format: FH5_RACE_FORMAT  # 이거는 게임 내에서 부르는 이름
    event: Optional[str]

    async def as_json(self):

        if not self.links_not_fetched:
            await self.fetch_all_links()

        return {
            "id": self.id_str,
            "name": self._prepare_names(),
            "nameTranslated": self._prepare_names_translated(),
            "description": self._prepare_descriptions(),
            "imageURLs": self.image_urls,
            "fullPathImage": self.full_path_image,
            "coordinateImages": self.coordinate_images,
            "iconURL": self.icon_url,
            "world": self.world,
            "laps": self.laps,
            "category": self.category,
            "raceFormat": self.race_format,
            "event": self.event,
        }

    async def indexedDB_race_route(self):
        _race_route = await self.as_json()
        _race_route.pop("imageURLs")
        _race_route.pop("fullPathImage")
        _race_route.pop("coordinateImages")
        return _race_route

    def indexedDB_Images_sync(self):

        coordiniateImages = [ci.as_json_sync() for ci in self.coordinate_images]

        return {
            "id": self.id_str,
            "imageURLs": self.image_urls,
            "fullPathImage": self.full_path_image,
            "coordinateImages": coordiniateImages,
            "iconURL": self.icon_url,
        }

    @property
    def links_not_fetched(self) -> bool:
        if isinstance(self.name, Link):
            return True
        if isinstance(self.description, Link):
            return True
        if isinstance(self.name_translated, Link):
            return True
        return False

    class Settings:
        name = "RaceRouteFH5"
        use_state_management = True
