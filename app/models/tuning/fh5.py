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

    def to_front(self):
        return

    def to_simple_front(self):

        carID = str(self.car.to_ref().id)

        # tags_ = [t.to_front_simple() for t in self.tags]
        tags_ = [str(t.id) for t in self.tags]

        detailedTuning_ = self.detailedTuning.model_dump(exclude_none=True)
        if not len(detailedTuning_.keys()):
            detailedTuning_ = None

        return {
            "id": str(self.id),
            "car": carID,
            "pi": self.pi,
            "tags": tags_,
            "share_code": self.share_code,
            "creator": self.creator,
            "detailedTuning": detailedTuning_,
            "performance": self.performance,
            "testReadings": self.testReadings,
            "tuningMajorParts": self.tuningMajorParts,
        }

    class Settings:
        name = "tuning_FH5"
        use_state_management = True
