"""Typed metadata for joining multi-omics layers without hiding batch effects."""

from dataclasses import dataclass
from enum import StrEnum


class OmicsLayer(StrEnum):
    GENOMICS = "genomics"
    EPIGENOMICS = "epigenomics"
    TRANSCRIPTOMICS = "transcriptomics"
    PROTEOMICS = "proteomics"
    METABOLOMICS = "metabolomics"
    MICROBIOMICS = "microbiomics"


@dataclass(frozen=True)
class MultiOmicsSample:
    sample_id: str
    participant_id: str
    layer: OmicsLayer
    features: dict[str, float | None]
    batch_id: str | None = None
    normalization: str | None = None


def integrate_samples(
    samples: list[MultiOmicsSample],
) -> dict[str, dict[str, dict[str, float | None]]]:
    """Group layers by common sample ID; missing values stay explicit as ``None``."""
    result: dict[str, dict[str, dict[str, float | None]]] = {}
    for sample in samples:
        if not sample.sample_id or not sample.participant_id:
            raise ValueError("sample_id and participant_id are required")
        result.setdefault(sample.sample_id, {})[sample.layer.value] = dict(sample.features)
    return result
