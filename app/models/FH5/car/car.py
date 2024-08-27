from app.models.deps.system import HasMultipleImages
from app.models.deps.xbox import ForzaHorizon

from ..base import FH5DocumentBase

from beanie import Link
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING
from ..components.car_details import CarBaseStat

if TYPE_CHECKING:
    from app.models.car import Car as CarOriginal


class Car(ForzaHorizon.BasedOnCar, HasMultipleImages, CarBaseStat, FH5DocumentBase):

    # base_car: Link[CarOriginal]

    # image_urls: List[Url] = Field(default=[])
    # first_image: Optional[Url]

    # PI: int = Field(ge=100, le=999)
    # meta: Meta
    # performance: Performance

    # TODO: 세부튜닝, 성능 수치, PI field, FH5 Meta 추가

    class Settings:
        name = "FH5.Car"
        is_root = True
