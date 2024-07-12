"""Decal models."""

from .base import DecalBase

__all__ = ("Decal_FH5",)


class Decal_FH5(DecalBase):

    # share_code
    # car
    # creator
    # imageURLs
    # firstImage
    # tags
    # first_uploaded
    # last_edited

    def to_front(self):
        """
        NOTE: call after fetching all links
        """
        return self.model_dump()

    def to_front_read(self):

        _partial = self.model_dump(
            include=[
                "id",
                "share_code",
                "creator",
                "imageURLs",
                "firstImage",
                "first_uploaded",
                "last_edited",
            ]
        )

        _car = self.car.to_simple()
        _tags = [t.to_simple() for t in self.tags]

        return {**_partial, "car": _car, "tags": _tags}

    class Settings:
        name = "decal_FH5"
        use_state_management = True
