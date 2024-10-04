from __future__ import annotations


from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException
from fastapi.websockets import WebSocketState
from pydantic import BaseModel, Field, field_serializer
import anyio
from typing import List, Dict, Any, Optional, Literal
import asyncio
from app.redis import r
import json
from pprint import pprint
from datetime import datetime
from random import randint
from app.utils.time import Datetime_Format, datetime_utc_format, datetime_utc
from enum import Enum


# 클라에서 받는 topic
class WS_RECEIVE_TOPIC(str, Enum):
    ping = "ping"
    dbStateCheck = "dbStateCheck"


# 클라한테 보내는 토픽
class WS_SEND_TOPIC(str, Enum):
    pong = "pong"
    dbState = "dbState"


__all__ = ("router",)


router = APIRouter(prefix="/ws", tags=["global", "websocket"])


def print_time(user: str) -> str:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"{user} : {current_time}")


def get_timestr() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


class WS_Receive_Base(BaseModel):
    topic: str
    GQM_ID: str


class DBStateResponse(BaseModel):
    table: str
    version: str
    lastUpdate: datetime

    @field_serializer("lastUpdate")
    def serialize_dt(self, dt: datetime, _info) -> int:
        # timestamp ms
        return int(dt.timestamp() * 1000)


class DBStateCheck(WS_Receive_Base):
    table: str

    def create_response(self):
        # FIXME:
        temp_version = "20240701-312"
        temp_lastUpdate = datetime_utc()
        return DBStateResponse(
            table=self.table, version=temp_version, lastUpdate=temp_lastUpdate
        )


async def dev_ws_receiver(websocket: WebSocket):

    SUB_KEY = f"CHAT_a"

    async for message in websocket.iter_json():
        pprint(message)
        # msg_json = json.loads(message)
        match message["topic"]:
            case WS_RECEIVE_TOPIC.ping:
                await websocket.send_json({"topic": "pong"})
            case WS_RECEIVE_TOPIC.dbStateCheck:
                dbStateCheck = DBStateCheck(**message)
                print(dbStateCheck)

                response = dbStateCheck.create_response()
                await websocket.send_json(
                    {"topic": WS_SEND_TOPIC.dbState, **response.model_dump()}
                )


async def dev_ws_str_receiver(websocket: WebSocket):

    SUB_KEY = f"CHAT_a"

    async for message in websocket.iter_bytes():
        pprint(message)
        # msg_json = json.loads(message)
        # print(f"{message['topic']=}")
        # match message["topic"]:
        #     case WS_RECEIVE_TOPIC.ping:
        #         pprint(message)
        #         await websocket.send_json({"topic": "pong", "message": get_timestr()})
        #     case WS_RECEIVE_TOPIC.dbStateCheck:
        #         print()
        #         await websocket.send_json({"topic": "pong", "message": get_timestr()})


async def dev_ws_sender(websocket: WebSocket):
    pubsub = r.pubsub()
    # await pubsub.subscribe(SUB_KEY, userInfo.redis_channel)

    while websocket.application_state != WebSocketState.DISCONNECTED:
        # async for message in pubsub.listen():
        #     pass
        # message 파싱해서 자신한테 맞는 메세지일 경우 받아서 처리하기
        # await websocket.send_json({"hello": "world"})
        await asyncio.sleep(5)


@router.websocket("")
async def dev_socket(websocket: WebSocket):

    await websocket.accept()

    async with anyio.create_task_group() as task_group:

        async def run_ws_receiver() -> None:
            await dev_ws_receiver(websocket)
            task_group.cancel_scope.cancel()

        task_group.start_soon(run_ws_receiver)
        # await dev_ws_sender(websocket)
