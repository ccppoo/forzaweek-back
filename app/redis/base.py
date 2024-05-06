import redis.asyncio as redis
import asyncio
from app.configs import redisSettings
from redis.commands.json.path import Path

from pprint import pprint


__all__ = ("r", "check_connection", "set_init_setup", "flush_all")

r = redis.from_url(redisSettings.URI)


async def check_connection(timeout: float = 3) -> bool:
    try:
        await asyncio.wait_for(r.ping(), timeout=timeout)
    except asyncio.TimeoutError:
        return False
    else:
        return True


async def set_init_setup():
    # 필수적으로 필요한 Redis key-value 미리 만들어 놓기
    pass
    # aaa = await r.json().set("ws_users", Path.root_path(), {"test": 123}, nx=True)


async def flush_all() -> bool:
    await r.flushall(asynchronous=False)
