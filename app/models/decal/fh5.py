"""Decal models."""

from .base import DecalBase

__all__ = ("Decal_FH5",)


class Decal_FH5(DecalBase):

    class Settings:
        name = "decal_FH5"
        use_state_management = True
