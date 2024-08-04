from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field
from beanie import Document, Link


T = TypeVar("T")


class Replyable(
    BaseModel,
    Generic[T],
):

    subComments: List[Link[T]] = Field(default=[])

    async def add_subcomment(self):
        pass
