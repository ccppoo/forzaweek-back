import yaml
import asyncio
from app.db.config import get_db_async, start_up_db
from app.models.car import Car
from app.models import Tuning, Car, CarTag, TrackTag, DifficultyTag, TuningTag
from app.models.FH5.race_route import RaceRoute
from app.models import models
from app.models.i18n import i18n, Locale
from app.configs import dbSettings
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie


FZ5_TRACK = "./samples/track.yaml"


async def get_tracks() -> list[Tuning]:
    tracks = []

    with open(FZ5_TRACK, mode="r", encoding="utf-8") as fp:
        tune = yaml.load(fp, Loader=yaml.FullLoader)

        for tt in tune["tracks"]:
            name = tt["name"]
            name_i18n = i18n(value=name["value"], ko=Locale(value=name["ko"]["value"]))
            type_ = tt["type"]
            type_i18n = i18n(
                value=type_["value"], ko=Locale(value=type_["ko"]["value"])
            )
            course = tt["course_type"]
            course_i18n = i18n(
                value=course["value"], ko=Locale(value=course["ko"]["value"])
            )
            track = RaceRoute(name=name_i18n, type=type_i18n, course_type=course_i18n)

            tracks.append(track)
    return tracks


async def main_async():
    db = AsyncIOMotorClient(dbSettings.URL)
    await init_beanie(db.forza, document_models=models)
    tracks = await get_tracks()
    for track in tracks:
        await track.insert()


if __name__ == "__main__":

    asyncio.run(main_async())
