from pydantic import BaseModel, Field

__all__ = ("Performance",)


class Performance(BaseModel):

    speed: float = Field(default=0, ge=0, le=10)
    handling: float = Field(default=0, ge=0, le=10)
    acceleration: float = Field(default=0, ge=0, le=10)
    launch: float = Field(default=0, ge=0, le=10)
    braking: float = Field(default=0, ge=0, le=10)
    offroad: float = Field(default=0, ge=0, le=10)
