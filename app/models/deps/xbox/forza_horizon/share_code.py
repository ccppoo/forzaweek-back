from pydantic import Field
from pprint import pprint
from pydantic import BaseModel

__all__ = ("HasShareCode",)


class HasShareCode(BaseModel):
    # ForzaHorizon

    share_code: str = Field(min_length=9, max_length=9)
