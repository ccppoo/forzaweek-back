from __future__ import annotations

from pprint import pprint
from pydantic import BaseModel, Field
from beanie import Link
from app.types.http import Url
from typing import List
from datetime import datetime


class Reward(BaseModel):
    car: str
    cloth: str
    emote: str
    forza_link: str
    super_wheel_spin: int
    wheel_spin: int
