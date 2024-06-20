"""Nation models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field
from typing import Literal, List


__all__ = ("FH5_meta",)


class FH5_meta(BaseModel):
    """FH5_meta"""

    division: str
    rarity: str
    boost: Optional[str]
    value: int = Field(ge=0)
