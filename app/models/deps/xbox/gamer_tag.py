from pydantic import Field
from pprint import pprint
from pydantic import BaseModel

__all__ = ("HasGamerTag",)


class HasGamerTag(BaseModel):

    gamer_tag: str = Field()
