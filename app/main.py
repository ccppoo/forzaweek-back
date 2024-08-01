from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import *
from app.websocket import *
from app.swagger import swaggerSettings
from app.logger import get_logger
from app.lifespan import lifespan


logger = get_logger()

app = FastAPI(**swaggerSettings.model_dump(), lifespan=lifespan)


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
app.include_router(indexedDBRouter)
app.include_router(tagKindRouter)
app.include_router(FH5Router)
app.include_router(AuthRouter)
# NOTE: remove dev router when release
app.include_router(devRouter)
# websocket
app.include_router(stateManageRouter)


@app.get("/")
async def get_resp():
    return "hello!"


@app.get("/global")
async def get_resp():
    return "hello!"
