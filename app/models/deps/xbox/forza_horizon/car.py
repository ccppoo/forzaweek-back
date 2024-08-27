from beanie import Document, Link
from pydantic import Field
from app.models.car import Car as CarOriginal
from pprint import pprint
from pydantic import BaseModel

__all__ = ("BasedOnCar",)


class BasedOnCar(BaseModel):
    # based on car

    base_car: Link[CarOriginal]
