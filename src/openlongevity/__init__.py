"""Evidence-first primitives for the OpenLongevity platform."""

from .evidence import EvidenceEngine, EvidenceLevel
from .models import EvidenceRecord, StudyType

__version__ = "0.1.0"

__all__ = ["EvidenceEngine", "EvidenceLevel", "EvidenceRecord", "StudyType", "__version__"]
