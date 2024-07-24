from pydantic import Field, BaseModel
from app.types import GAME


class GameBase(BaseModel):
    game: GAME
