from typing import Optional

from pydantic import BaseModel, Field


__all__ = ("Meta",)


class Meta(BaseModel):
    """FH5_meta"""

    division: str
    rarity: str
    boost: Optional[str]
    value: int = Field(ge=0)
