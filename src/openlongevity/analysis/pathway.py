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
    """Compute one-sided pathway enrichment with monotonic Benjamini-Hochberg q-values.

    The multiple-testing family is every pathway that has at least one member inside the
    supplied universe. Pathways with no observed overlap still contribute to the
    correction factor, because excluding them would make adjusted p-values depend on
    the observed result rather than the declared hypothesis family. The returned list
    remains focused on pathways with at least one overlapping gene.
    """
    if not genes or not pathways or not universe or not genes <= universe:
        raise ValueError("genes must be non-empty and contained in universe")
    tests: list[tuple[str, int, int, float]] = []
    sample_size = len(genes)
    population_size = len(universe)
    for name, members in pathways.items():
        overlap = len(genes & members)
        size = len(members & universe)
        if not size:
            continue
        if overlap:
            tail = sum(
                comb(size, k) * comb(population_size - size, sample_size - k)
                for k in range(overlap, min(size, sample_size) + 1)
                if sample_size - k <= population_size - size
            )
            denominator = comb(population_size, sample_size)
            p_value = min(1.0, tail / denominator)
        else:
            p_value = 1.0
        tests.append((name, overlap, size, p_value))
    tests.sort(key=lambda item: (item[3], item[0]))

    adjusted_by_pathway: dict[str, float] = {}
    running_adjusted = 1.0
    family_size = len(tests)
    for rank, (name, _overlap, _size, p_value) in reversed(
        list(enumerate(tests, start=1))
    ):
        running_adjusted = min(running_adjusted, min(1.0, p_value * family_size / rank))
        adjusted_by_pathway[name] = running_adjusted

    return [
        EnrichmentResult(name, overlap, size, p, adjusted_by_pathway[name])
        for name, overlap, size, p in tests
        if overlap
    ]
