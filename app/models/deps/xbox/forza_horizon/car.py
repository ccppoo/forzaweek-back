from beanie import Document, Link
from pydantic import Field
from app.models.car import Car as CarOriginal
from pprint import pprint
from pydantic import BaseModel
from typing import Optional


__all__ = ("BasedOnCar",)


class BasedOnCar(BaseModel):
    # based on car

    car: Link[CarOriginal]
    edition: Optional[str] = Field(None, description="anniversary, forza, donut")
