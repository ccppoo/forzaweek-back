from fastapi import FastAPI

from app.routers import *
from app.swagger import swaggerSettings
from app.db.config import start_up_db
from app.logger import get_logger
from fastapi.middleware.cors import CORSMiddleware

logger = get_logger()

app = FastAPI(**swaggerSettings.model_dump())


origins = [
    "https://localhost",
    "https://localhost:5173",
    "https://localhost:5174",
    "https://localhost:5151",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "PUT", "GET", "OPTIONS", "HEAD", "DELETE"],
    allow_headers=["*"],
)

# app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())

app.include_router(devRouter)
app.include_router(imageRouter)
app.include_router(nationRouter)
app.include_router(manufacturerRouter)
app.include_router(carRouter)
app.include_router(dataRouter)
app.include_router(tagRouter)


@app.get("/")
async def get_resp():
    return "hello!"


@app.get("/global")
async def get_resp():
    return "hello!"


@app.on_event("startup")
async def on_startup():
    # from app.redis import check_connection, flush_all, set_init_setup
    # from app.configs import redisSettings

    from argparser import args

    # redis
    # if not await check_connection():
    #     print(f"Failed to Connect Redis (URI : {redisSettings.URI})")
    #     exit(-1)

    # await set_init_setup()

    # # NOTE: 개발 단계에서만 사용
    # await flush_all()  # 재시작 이후 초기화
    logger.info("startup complete")
    await start_up_db(app)


@app.on_event("shutdown")
async def on_shutdown():
    # shutdown process
    logger.info("shutdown complete")
