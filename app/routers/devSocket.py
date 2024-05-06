from __future__ import annotations
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException
from fastapi.websockets import WebSocketState
from pydantic import BaseModel, Field
import anyio
from typing import List, Dict, Any, Optional
import asyncio

import json
from pprint import pprint
from datetime import datetime

from random import randint


__all__ = ("router",)


router = APIRouter(prefix="", tags=["global"])


def print_time(user: str) -> str:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"{user} : {current_time}")


def get_timestr() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_random_int(from_: int, to_: int):
    return randint(from_, to_)


def get_random_monitoring(name: str):
    match name:
        case "cpu":
            a = [40 - get_random_int(10, 30) for _ in range(4)]
            return {
                "subject": "cpu",
                "temperature": get_random_int(40, 80),
                "total_usage": get_random_int(10, 70),
                "core_usage": a,
            }
        case "memory":
            return {
                "subject": "memory",
                "total": 64,
                "usage": get_random_int(15, 60),
            }


async def ws_receiver(websocket: WebSocket):
    SUB_KEY = f"CHAT_a"

    async for message in websocket.iter_json():
        msg_json = json.loads(message)
        pprint(msg_json)
        # print(f"{message['type']=}")
        match message["type"]:
            case "ping":
                await websocket.send_json({"topic": "pong", "message": get_timestr()})


async def ws_sender(websocket: WebSocket, id: int):
    SUB_KEY = f"CHAT_a"

    while websocket.application_state != WebSocketState.DISCONNECTED:
        await asyncio.sleep(1)
        await websocket.send_json({"topic": "pong", "id": id, "message": get_timestr()})


async def dev_ws_receiver(websocket: WebSocket):
    SUB_KEY = f"CHAT_a"

    async for message in websocket.iter_json():
        msg_json = json.loads(message)
        pprint(msg_json)
        # print(f"{message['type']=}")
        match message["type"]:
            case "ping":
                await websocket.send_json({"topic": "pong", "message": get_timestr()})


async def dev_ws_sender(websocket: WebSocket):
    while websocket.application_state != WebSocketState.DISCONNECTED:
        cpu_, mem_ = get_random_monitoring("cpu"), get_random_monitoring("memory")
        await websocket.send_json({"topic": "monitoring", "cpu": cpu_, "memory": mem_})
        await asyncio.sleep(2)


@router.websocket("/dev/{id}")
async def dev_socket(websocket: WebSocket, id: int):

    await websocket.accept()

    async with anyio.create_task_group() as task_group:

        async def run_ws_receiver() -> None:
            await ws_receiver(websocket)
            task_group.cancel_scope.cancel()

        task_group.start_soon(run_ws_receiver)
        await ws_sender(websocket, id)


@router.websocket("/all")
async def dev_socket(websocket: WebSocket):

    await websocket.accept()

    async with anyio.create_task_group() as task_group:

        async def run_ws_receiver() -> None:
            await dev_ws_sender(websocket)
            task_group.cancel_scope.cancel()

        task_group.start_soon(run_ws_receiver)
        await dev_ws_sender(websocket)
