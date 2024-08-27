from pydantic import Field, BaseModel
from app.types import GAME

__all__ = ("GameBase",)


class GameBase(BaseModel):
    game: GAME
