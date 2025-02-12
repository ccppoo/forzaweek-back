from typing import Optional
from pydantic import BaseModel, Field
from .aero import Aero
from .tires import Tiers
from .gearing import Gearing
from .alignment import Alignment
from .antiroll_bars import AntirollBars
from .springs import Springs
from .damping import Damping
from .aero import Aero
from .brake import Brake
from .diffrential import Differntial

__all__ = ("DetailedTunings",)


class DetailedTunings(BaseModel):
    """

    NOTE: 튜닝마다 활성화된 옵션이 모두 다르고, 입력을 안할 수 있으므로 모두 Optional로 설정
    """

    tires: Optional[Tiers] = Field(default=None)
    gearing: Optional[Gearing] = Field(default=None)
    alignment: Optional[Alignment] = Field(default=None)
    antirollBars: Optional[AntirollBars] = Field(default=None)
    springs: Optional[Springs] = Field(default=None)
    damping: Optional[Damping] = Field(default=None)
    aero: Optional[Aero] = Field(default=None)
    brake: Optional[Brake] = Field(default=None)
    diffrential: Optional[Differntial] = Field(default=None)
