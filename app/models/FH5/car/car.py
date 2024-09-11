from app.models.deps.system import HasMultipleImages
from app.models.deps.xbox import ForzaHorizon

from ..base import FH5DocumentBase

from beanie import Link
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING, List, Literal, Optional
from ..components.car_details import CarBaseStat
from app.models.car import Car

# if TYPE_CHECKING:
#     from app.models.car import Car as CarOriginal


class Car_FH5(HasMultipleImages, CarBaseStat, FH5DocumentBase):

    base_car: Link[Car]
    edition: Optional[str] = Field(None, description="anniversary, forza, donut")
    # base_car: Link[CarOriginal]
    # edition -> Forizon Edition, Anniversary, 등

    # image_urls: List[Url] = Field(default=[])
    # first_image: Optional[Url]

    # PI: int = Field(ge=100, le=999)
    # meta: Meta
    # performance: Performance

    async def as_json(self, *, base_car_as_id: bool = True):

        base_car = str(self.base_car.to_ref().id)
        if not base_car_as_id and not self.links_not_fetched:
            await self.fetch_all_links()
            base_car = await self.base_car.as_json()

        return {
            "id": self.id_str,
            "baseCar": base_car,
            "PI": self.PI,
            "meta": self.meta,
            "imageURLs": self.image_urls,
            "performance": self.performance,
        }

    async def indexedDB_car(self):
        _car = await self.as_json()
        _car.pop("imageURLs")
        return _car

    def indexedDB_Images_sync(self):
        return {
            "id": self.id_str,
            "imageURLs": self.image_urls,
        }

    @property
    def links_not_fetched(self) -> bool:
        if isinstance(self.base_car, Link):
            return True
        return False

    # TODO: 세부튜닝, 성능 수치, PI field, FH5 Meta 추가

    class Settings:
        name = "FH5_Car"
