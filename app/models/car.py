"""Car models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr, Field
from typing import Literal, List, Union
from .manufacturer import Manufacturer
from .driveTrain import DriveTrain
from .bodyStyle import BodyStyle
from .i18n import i18n
from .engine import Engine
from app.types.http import Url
from .component.fh5 import FH5_meta
from pprint import pprint

__all__ = ("Car", "dbInit")

PI_RANKS = ["D", "C", "B", "A", "S1", "S2", "X"]
RARITY_LITERAL = [
    "Common",
    "Rare",
    "Epic",
    "Legendary",
    "Forza Edition",
    "Anniversary Edition",
]


class CarName(i18n):
    # value : str
    # lang: str
    pass


class CarShortName(i18n):
    # value : str
    # lang: str
    pass


class Car(Document):
    """Car DB representation."""

    manufacturer: Link[Manufacturer]

    images: List[Url]
    first_image: Optional[Url]

    production_year: int = Field(ge=1900, le=2560)
    engine_type: str
    body_style: str
    door: int = Field(ge=0)

    name_en: str
    name: List[Link[CarName]]

    short_name_en: str
    short_name: List[Link[CarShortName]]

    fh5_meta: FH5_meta

    @property
    def created(self) -> datetime | None:
        """Datetime car was created from ID."""
        return self.id.generation_time if self.id else None

    async def to_json(self, lang: str):

        abbrieve = None
        for abv in self.abbreviation:
            if abv.lang == lang:
                abbrieve = abv.value
                break
        name = None
        for na in self.name:
            if na.lang == lang:
                name = na.value

        manu = None
        if isinstance(self.manufacturer, Link):
            print(f"{self.manufacturer=}")
            mmm = await self.manufacturer.fetch(fetch_links=True)
            manu = mmm.to_json()
            # await self.fetch_link("manufacturer")
        else:
            manu = self.manufacturer.to_json(lang)

        # TODO: engine 세부 정보 찾아서 넣어주기

        engineTypeName = None
        for engineTname in self.engineType:
            # print(f"{engineTname=}")
            if engineTname.lang == lang:
                engineTypeName = engineTname.value
                break

        # TODO: driveTrain 세부 정보 찾아서 넣어주기

        # NOTE: DriveTrainTypeName는 AWD, RWD, FWD -> 번역본 셋 중 하나
        driveTrainTypeName = None
        for dtname in self.driveTrainType:
            if dtname.lang == lang:
                driveTrainTypeName = dtname.value
                break

        return {
            "name": name,
            "abbreviation": abbrieve,
            "manufacturer": manu,
            "bodyStyle": self.bodyStyle.get_value(lang),
            "driveTrainType": driveTrainTypeName,
            "driveTrain": None,
            "engineType": engineTypeName,
            "engine": None,
            "year": self.year,
            "door": self.door,
            "lang": lang,
        }

    async def to_json_all_lang(self, _id: bool = False) -> dict[str, Any]:
        # await self.fetch_all_links()
        # 직접 id 가져오는 방법?

        name = [x.model_dump(include=["value", "lang"]) for x in self.name]
        short_name = [x.model_dump(include=["value", "lang"]) for x in self.name]

        _id = self.model_dump(include=["id"])["id"]
        return {
            "id": _id,
            "manufacturer": self.manufacturer.to_json_all_lang(),
            "name_en": self.name_en,
            "name": name,
            "short_name_en": self.short_name_en,
            "short_name": short_name,
            "imageURLs": self.images,
            "firstImage": self.first_image,
            "production_year": self.production_year,
            "engineType": self.engine_type,
            "bodyStyle": self.body_style,
            "door": self.door,
            "fh5_meta": self.fh5_meta,
        }

    async def to_json_edit(self) -> dict[str, Any]:
        # print(self.manufacturer.to_ref().id)

        await self.fetch_link(Car.name)
        await self.fetch_link(Car.short_name)

        name = [x.model_dump(include=["value", "lang"]) for x in self.name]
        short_name = [x.model_dump(include=["value", "lang"]) for x in self.short_name]

        aa = {
            "id": str(self.id),
            "manufacturer": str(self.manufacturer.to_ref().id),
            "name_en": self.name_en,
            "name": name,
            "short_name_en": self.short_name_en,
            "short_name": short_name,
            "imageURLs": self.images,
            "firstImage": self.first_image,
            "production_year": self.production_year,
            "engineType": self.engine_type,
            "bodyStyle": self.body_style,
            "door": self.door,
            "fh5_meta": self.fh5_meta,
        }
        return aa

    class Settings:
        name = "car"
        use_state_management = True


dbInit = (
    Car,
    CarName,
    CarShortName,
)
