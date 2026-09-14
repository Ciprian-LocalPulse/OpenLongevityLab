"""Pathway enrichment interface using a hypergeometric tail and BH correction."""

from dataclasses import dataclass
from math import comb


@dataclass(frozen=True)
class EnrichmentResult:
    pathway: str
    overlap: int
    pathway_size: int
    p_value: float
    adjusted_p_value: float


def enrich_gene_set(
    genes: set[str], pathways: dict[str, set[str]], universe: set[str]
) -> list[EnrichmentResult]:
    if not genes or not pathways or not universe or not genes <= universe:
        raise ValueError("genes must be non-empty and contained in universe")
    tests: list[tuple[str, int, int, float]] = []
    sample_size = len(genes)
    population_size = len(universe)
    for name, members in pathways.items():
        overlap = len(genes & members)
        size = len(members & universe)
        if not size or not overlap:
            continue
        tail = sum(
            comb(size, k) * comb(population_size - size, sample_size - k)
            for k in range(overlap, min(size, sample_size) + 1)
            if sample_size - k <= population_size - size
        )
        denominator = comb(population_size, sample_size)
        tests.append((name, overlap, size, min(1.0, tail / denominator)))
    tests.sort(key=lambda item: item[3])
    return [
        EnrichmentResult(name, overlap, size, p, min(1.0, p * len(tests) / rank))
        for rank, (name, overlap, size, p) in enumerate(tests, 1)
    ]
