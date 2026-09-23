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
    """Group layers by common sample ID; missing values stay explicit as ``None``.

    A sample identifier must map to a single participant, and each sample/layer pair
    may appear only once. Silent overwrites are rejected because they can hide
    participant mix-ups, repeated exports, or inconsistent upstream normalization.
    """
    result: dict[str, dict[str, dict[str, float | None]]] = {}
    participants_by_sample: dict[str, str] = {}
    for sample in samples:
        if not sample.sample_id or not sample.participant_id:
            raise ValueError("sample_id and participant_id are required")
        previous_participant = participants_by_sample.setdefault(
            sample.sample_id, sample.participant_id
        )
        if previous_participant != sample.participant_id:
            raise ValueError("sample_id must map to exactly one participant_id")

        layers = result.setdefault(sample.sample_id, {})
        if sample.layer.value in layers:
            raise ValueError("duplicate sample_id and layer combination")
        layers[sample.layer.value] = dict(sample.features)
    return result
