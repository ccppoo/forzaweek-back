from __future__ import annotations

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4


class UserInfo(BaseModel):
    username: str
    uid: str

    @property
    def redis_channel(self) -> str:
        return f"{self.username}.{self.uid}"

    def __eq__(self, __value: UserInfo) -> bool:
        return self.username == __value.username and self.uid == __value.uid


class UserInit(BaseModel):
    type: str = "user_init"
    username: str
    uid: str = Field(default_factory=lambda: str(uuid4()))

    def create_reply(self) -> dict:
        return {"type": "SET_USERNAME", 'username' :self.username , "uid": self.uid}

    def get_userInfo(self) -> UserInfo:
        return UserInfo(username=self.username, uid=self.uid)


class ConnectionInit(BaseModel):
    type: str = "connection_init"
    uid: str = Field(default_factory=lambda: str(uuid4()))

    def create_reply(self) -> dict:
        return {"type": "CONN_INIT", "uid": self.uid}

class Ping(BaseModel):
    type: str = "ping"
    username: str
    uid: str

    def create_reply(self) -> dict:
        dt = str(datetime.now())
        return {"type": "PONG", "timestamp": dt}
