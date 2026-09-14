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
    confounders: tuple[str, ...] = ()
    source_references: tuple[str, ...] = ()


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
        ("Cell composition", "Tissue choice", "Technical batch effects"),
    ),
    BiomarkerDefinition(
        "telomere length",
        BiomarkerCategory.TELOMERE,
        "Relative or absolute telomeric DNA length",
        "A component of cellular replicative history",
        ("Large inter-individual variation", "Assay and cell-type effects"),
        "heterogeneous",
        ("Cell type", "Assay platform", "Inherited variation"),
    ),
    BiomarkerDefinition(
        "C-reactive protein",
        BiomarkerCategory.INFLAMMATORY,
        "Circulating acute-phase protein concentration",
        "A nonspecific marker of systemic inflammation in population studies",
        ("Acute infection and injury can dominate the signal", "Not specific to aging"),
        "established measurement; context-dependent aging evidence",
        ("Infection", "Adiposity", "Medication", "Smoking"),
    ),
    BiomarkerDefinition(
        "interleukin-6",
        BiomarkerCategory.INFLAMMATORY,
        "Circulating cytokine concentration",
        "Inflammatory signaling research and cohort stratification",
        ("High assay variability", "Pleiotropic biology", "Short-term fluctuations"),
        "research marker",
        ("Acute illness", "Exercise", "Circadian timing"),
    ),
    BiomarkerDefinition(
        "HbA1c",
        BiomarkerCategory.METABOLOMIC,
        "Glycated hemoglobin percentage",
        "Longer-window glycemic state for metabolic aging studies",
        ("Red-cell lifespan changes affect interpretation", "Not an aging-specific marker"),
        "clinically standardized assay; aging interpretation varies",
        ("Anemia", "Hemoglobin variants", "Renal disease"),
    ),
    BiomarkerDefinition(
        "immune-cell composition",
        BiomarkerCategory.IMMUNE,
        "Relative abundance of defined immune-cell populations",
        "Characterizes immune remodeling across age and cohorts",
        ("Flow cytometry panels are not interchangeable", "Relative abundance is compositional"),
        "research marker",
        ("Collection time", "Tissue source", "Panel design"),
    ),
    BiomarkerDefinition(
        "CDKN2A/p16-related signal",
        BiomarkerCategory.SENESCENCE,
        "Expression or protein signal used in a defined cellular context",
        "One component of senescence-oriented assays",
        ("Context and cell type are essential", "No single marker defines senescence"),
        "preclinical and assay-specific",
        ("Cell type", "Assay specificity", "Tissue heterogeneity"),
    ),
    BiomarkerDefinition(
        "mitochondrial respiration",
        BiomarkerCategory.MITOCHONDRIAL,
        "Oxygen consumption or related functional readout",
        "Functional characterization of mitochondrial physiology",
        ("Protocol and instrument dependent", "Cell state strongly affects results"),
        "research assay",
        ("Substrate choice", "Cell density", "Temperature"),
    ),
    BiomarkerDefinition(
        "age-associated proteomic signature",
        BiomarkerCategory.PROTEOMIC,
        "Panel of circulating protein measurements",
        "Multivariate association with age-related phenotypes",
        ("Platform and cohort transferability", "Model overfitting risk"),
        "emerging research",
        ("Assay platform", "Cohort composition", "Pre-analytics"),
    ),
    BiomarkerDefinition(
        "age-associated transcriptomic signature",
        BiomarkerCategory.TRANSCRIPTOMIC,
        "Expression profile across a defined tissue or cell population",
        "Molecular characterization of age-associated programs",
        ("Tissue specificity", "Cell composition", "Batch effects"),
        "emerging research",
        ("RNA quality", "Library preparation", "Tissue composition"),
    ),
)


def find(name: str) -> list[BiomarkerDefinition]:
    needle = name.casefold().strip()
    return [
        item for item in CATALOG if needle in item.name.casefold() or needle == item.category.value
    ]
