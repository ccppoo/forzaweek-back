from app.models.deps.system import HasUploader
from app.models.deps.xbox import SharingCreativeWorks
from ..base import FH5DocumentBase
from app.models.FH5.car import Car_FH5
from app.models.FH5.components.car_details import CarTuningStat
from beanie import Link
from pydantic import BaseModel, Field


class Tuning(SharingCreativeWorks, HasUploader, CarTuningStat, FH5DocumentBase):

    # share_code: str = Field(min_length=9, max_length=9)
    # gamer_tag: str = Field()

    # PI: int = Field(ge=100, le=999)
    # performance: Performance
    # detailedTuning: DetailedTunings
    # testReadings: TestReadings
    # tuningMajorParts: MajorParts

    # uploader: str
    name: str

    base_car_fh5: Link[Car_FH5]

    # TODO: 세부튜닝, 성능 수치, PI field 추가

    async def as_json(self):

        return {
            "shareCode": self.share_code,
            "gamerTag": self.gamer_tag,
            "name": self.name,
            "pi": self.PI,
            "performance": self.performance,
            "detailedTuning": self.detailedTuning,
            "testReadings": self.testReadings,
            "tuningMajorParts": self.tuningMajorParts,
            "uploader": self.uploader,
        }

    class Settings:
        name = "FH5_Tuning"
        is_root = True
