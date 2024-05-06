from dataclasses import dataclass
from redis.commands.json.path import Path

# from ..redis import r
# from app.configs import redisSettings
# import redis.asyncio as redis
from .base import r
# r = redis.from_url(redisSettings.URI)

from pprint import pprint


def Room_Name(name: str) -> str:
    return f"room-{name}"


@dataclass
class UserManager:
    # _rooms  : set = set()

    @staticmethod
    async def create_user( username: str, uid : str):
        # 방 생성(방장)
        registerUserPath = Path.root_path()
        print(f'{registerUserPath=}')
        await r.json().set('ws_users', registerUserPath,  {uid : {'name' : username}}, decode_keys=True)

        return

    @staticmethod
    async def remove_user(room_name: str, user_name: str) -> list[str]:
        # 방 없애고, 방에 있는 다른 사람들 이름 리스트 반환
        ROOM_RELAY_KEY = f"RELAY-{room_name}"

        if not await r.json().get(room_name):
            return
        _users = await r.json().get(room_name, "users")

        await r.json().delete(room_name, Path.root_path())
        await r.srem(ROOM_RELAY_KEY, user_name)

        return _users

