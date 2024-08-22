from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette import status
from app.routers import *
from app.websocket import *
from app.swagger import swaggerSettings
from app.logger import get_logger
from app.lifespan import lifespan

from fastapi.exceptions import RequestValidationError

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
    allow_methods=["POST", "PUT", "GET", "OPTIONS", "PATCH", "HEAD", "DELETE"],
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
app.include_router(FH5Router)
app.include_router(AuthRouter)
app.include_router(userRouter)
app.include_router(commentRouter)
app.include_router(boardRouter)
app.include_router(searchRouter)
# NOTE: remove dev router when release
app.include_router(devRouter)
# websocket
app.include_router(stateManageRouter)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    # return
    # WARNING: Only for DEV
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.get("/")
async def get_resp():
    return "hello!"


@app.get("/global")
async def get_resp():
    return "hello!"
