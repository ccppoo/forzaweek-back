from app.models.tuning.base import TuningBase
from app.models.stat.fh5 import TuningStat_FH5

__all__ = ("Tuning_FH5",)


class Tuning_FH5(TuningBase, TuningStat_FH5):
    """FH5 Tuning DB representation."""

    # share_code
    # car
    # creator
    # tags

    # detailedTuning
    # performance
    # testReadings
    # tuningMajorParts

    class Settings:
        name = "tuning_FH5"
        use_state_management = True
