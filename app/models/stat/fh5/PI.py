from pydantic import BaseModel, Field

__all__ = ("PI",)


class PI(BaseModel):
    pi: int = Field(ge=100, le=999)
