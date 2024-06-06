"""Car models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr, Field
from typing import Literal, List
from .manufacturer import Manufacturer
from .driveTrain import DriveTrain
from .bodyStyle import BodyStyle
from .i18n import i18n
from .engine import Engine


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


class CarAbbreviation(i18n):
    # value : str
    # lang: str
    pass


class DriveTrainTypeName(i18n):
    pass


class EngineTypeName(i18n):
    pass


class Car(Document):
    """Car DB representation."""

    name: List[Link[CarName]]
    abbreviation: List[Link[CarAbbreviation]]
    manufacturer: Link[Manufacturer]
    bodyStyle: Link[BodyStyle]
    driveTrainType: List[Link[DriveTrainTypeName]]
    driveTrain: Optional[Link[DriveTrain]]
    engineType: List[Link[EngineTypeName]]
    engine: Optional[Link[Engine]]
    year: int
    door: int = Field(default=0)

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
            print("asdasdasd")
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

    class Settings:
        name = "car"


dbInit = (
    Car,
    CarName,
    CarAbbreviation,
    DriveTrainTypeName,
    EngineTypeName,
)
