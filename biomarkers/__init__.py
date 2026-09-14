"""Biomarker category definitions and interpretation guardrails."""
from dataclasses import dataclass
from enum import StrEnum


class BiomarkerCategory(StrEnum):
    EPIGENETIC = "epigenetic"
    PROTEOMIC = "proteomic"
    TRANSCRIPTOMIC = "transcriptomic"
    METABOLOMIC = "metabolomic"
    INFLAMMATORY = "inflammatory"
    IMMUNE = "immune"
    MITOCHONDRIAL = "mitochondrial"
    SENESCENCE = "cellular_senescence"
    TELOMERE = "telomere"


@dataclass(frozen=True)
class BiomarkerDefinition:
    name: str
    category: BiomarkerCategory
    measured: str
    relevance: str
    limitations: tuple[str, ...]
    evidence_maturity: str


CATALOG = (
    BiomarkerDefinition(
        "epigenetic age estimate",
        BiomarkerCategory.EPIGENETIC,
        "DNA methylation patterns at a defined panel of loci",
        "Population-level association with age-related phenotypes",
        (
            "Clock calibration varies by tissue and cohort",
            "Not a definitive measure of biological age",
        ),
        "varies by clock and validation cohort",
    ),
    BiomarkerDefinition(
        "telomere length",
        BiomarkerCategory.TELOMERE,
        "Relative or absolute telomeric DNA length",
        "A component of cellular replicative history",
        ("Large inter-individual variation", "Assay and cell-type effects"),
        "heterogeneous",
    ),
)


def find(name: str) -> list[BiomarkerDefinition]:
    needle = name.casefold().strip()
    return [
        item
        for item in CATALOG
        if needle in item.name.casefold() or needle == item.category.value
    ]
