"""Evidence-first primitives for the OpenLongevity platform."""
__version__ = "0.1.0"
from .evidence import EvidenceEngine, EvidenceLevel
from .models import EvidenceRecord, StudyType
__all__ = ["EvidenceEngine", "EvidenceLevel", "EvidenceRecord", "StudyType", "__version__"]
