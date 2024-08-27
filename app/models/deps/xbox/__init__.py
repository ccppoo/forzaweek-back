import app.models.deps.xbox.forza_horizon as ForzaHorizon

from .gamer_tag import *


class SharingCreativeWorks(ForzaHorizon.HasShareCode, HasGamerTag):
    pass


class ForzaHorizonDecal(ForzaHorizon.BasedOnCar, SharingCreativeWorks):
    pass


class ForzaHorizonTuning(ForzaHorizon.BasedOnCar, SharingCreativeWorks):
    pass


class ForzaHorizonVinylGroups(SharingCreativeWorks):
    pass
