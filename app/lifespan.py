from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.logger import get_logger
from app.db.config import start_up_db


__all__ = ("lifespan",)

logger = get_logger()


async def on_startup(app: FastAPI):
    from app.redis import check_connection, flush_all, set_init_setup
    from app.configs import redisSettings
    from argparser import args

    # redis
    if not await check_connection():
        print(f"Failed to Connect Redis (URI : {redisSettings.URI})")
        exit(-1)
    else:
        logger.info("redis online")

    await set_init_setup()

    # WARNING: 개발 단계에서만 사용
    await flush_all()  # 재시작 이후 초기화
    logger.info("startup complete")
    await start_up_db(app)


async def on_shutdown():
    # shutdown process
    logger.info("shutdown complete")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup(app)

    yield

    await on_shutdown()
