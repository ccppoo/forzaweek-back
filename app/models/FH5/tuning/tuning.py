from app.models.deps.system import HasUploader
from app.models.deps.xbox import SharingCreativeWorks, ForzaHorizonTuning
from ..base import FH5DocumentBase
from app.models.FH5.car import Car_FH5
from app.models.FH5.components.car_details import CarTuningStat
from beanie import Link
from pydantic import BaseModel, Field


class Tuning(ForzaHorizonTuning, HasUploader, CarTuningStat, FH5DocumentBase):

    # base_car: Link[CarOriginal]
    # share_code: str = Field(min_length=9, max_length=9)
    # gamer_tag: str = Field()

    # PI: int = Field(ge=100, le=999)
    # performance: Performance
    # detailedTuning: DetailedTunings
    # testReadings: TestReadings
    # tuningMajorParts: MajorParts

    # uploader: str

    base_car_fh5: Link[Car_FH5]

    # TODO: 세부튜닝, 성능 수치, PI field 추가

    class Settings:
        name = "FH5.Tuning"
        is_root = True
