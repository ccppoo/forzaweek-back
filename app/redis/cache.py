from dataclasses import dataclass
from redis.commands.json.path import Path

from .base import r
from app.types import TIME_SEGMENT, MARKET_SEGMENT
from pprint import pprint

__all__ = ("MarketStatCache",)


def Room_Name(name: str) -> str:
    return f"room-{name}"


@dataclass
class MarketStatCache:

    def generate_key(market_seg: MARKET_SEGMENT, time_seg: TIME_SEGMENT) -> str:

        return ""

    @staticmethod
    async def save(market_seg: MARKET_SEGMENT, time_seg: TIME_SEGMENT):
        # 방 생성(방장)
        # print("creating room")

        MarketStatCache.generate_key(market_seg, time_seg)
        return
        await r.json().set(room_name, Path.root_path(), {"users": [user_name]})

        _json = await r.json().get(room_name)
        if _json:
            pass
        await r.sadd(ROOM_RELAY_KEY, user_name)
        # _json = await r.json().get(room_name)
        # pprint(_json)
        return
