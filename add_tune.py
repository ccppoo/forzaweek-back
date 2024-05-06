import yaml
import asyncio
from app.db.config import get_db_async, start_up_db
from app.models.car import Car
from app.models.car_stat import CarStat
from app.models import Tuning, Car, CarTag, TrackTag, DifficultyTag, TuningTag
from app.models import models
from app.configs import dbSettings
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie


FZ5_TUNE = "tune.yaml"


async def get_tune() -> list[Tuning]:
    tunings = []
    with open(FZ5_TUNE, mode="r") as fp:
        tune = yaml.load(fp, Loader=yaml.FullLoader)

        for tt in tune["A"]:
            car = await Car.find_one(Car.name == tt["car"])
            tags = []
            for k, vv in tt["tags"].items():
                if k == "track":
                    for v in vv:
                        trackTag = await TrackTag.find_one(TrackTag.name == v)
                        if not trackTag:
                            trackTag = TrackTag(name=v)
                            await trackTag.insert()
                        tags.append(trackTag)
                if k == "tuning":
                    for v in vv:
                        tuningTag = await TuningTag.find_one(TuningTag.name == v)
                        if not tuningTag:
                            tuningTag = TuningTag(name=v)
                            await tuningTag.insert()
                        tags.append(tuningTag)

            car_stat = CarStat(PI=800)

            tuning = Tuning(
                car=car,
                creator=tt["creator"],
                share_code=tt["share_code"],
                tags=tags,
                stat=car_stat,
            )
            tunings.append(tuning)
    return tunings


async def main_async():
    db = AsyncIOMotorClient(dbSettings.URL)
    await init_beanie(db.forza, document_models=models)
    tunes = await get_tune()
    for tune in tunes:
        await tune.insert()


if __name__ == "__main__":

    asyncio.run(main_async())
