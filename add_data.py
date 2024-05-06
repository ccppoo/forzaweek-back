import csv
import asyncio
from app.db.config import get_db_async, start_up_db
from app.models.car import Car, CarStat
from app.models import models
from app.configs import dbSettings
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie


FZ5_CARLIST = "fh5_cars.csv"


def get_cars() -> list[Car]:
    cars = []
    with open(FZ5_CARLIST, mode="r", encoding="utf-8") as fp:
        reader = csv.reader(fp)
        cnt = 0
        next(reader)
        for line in reader:
            (
                name,
                manufacture,
                year,
                model,
                type_,
                rarity,
                _,
                country,
                _,
                value,
                *res,
            ) = line
            _, pi, speed, handling, accel, launch, braking, offroad = res
            cs = CarStat(
                speed=speed,
                handling=handling,
                acceleration=accel,
                launch=launch,
                braking=braking,
                offroad=offroad,
                PI=pi,
            )

            value = int(value.replace("CR", "").replace(",", "").strip())
            car = Car(
                name=name,
                manufacturer=manufacture,
                year=year,
                model=model,
                type=type_,
                rarity=rarity,
                country=country,
                value=value,
                stat=cs,
            )
            cars.append(car)
    return cars


async def main_async():
    db = AsyncIOMotorClient(dbSettings.URL)
    await init_beanie(db.forza, document_models=models)
    cars = get_cars()
    for car in cars:
        await car.insert()


if __name__ == "__main__":

    asyncio.run(main_async())
