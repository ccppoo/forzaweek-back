from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.configs import dbSettings
from app.models import models


async def start_up_db(app: FastAPI):
    app.db = AsyncIOMotorClient(dbSettings.URL).account
    await init_beanie(app.db, document_models=models)


async def get_db_async():
    return AsyncIOMotorClient(dbSettings.URL)
