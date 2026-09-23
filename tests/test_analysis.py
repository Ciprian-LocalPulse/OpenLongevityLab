from openlongevity.analysis.biological_age import BiologicalAgeModel
from openlongevity.analysis.omics import MultiOmicsSample, OmicsLayer, integrate_samples
from openlongevity.analysis.pathway import enrich_gene_set
from openlongevity.analysis.survival import kaplan_meier


def test_biological_age_baseline_reports_metrics() -> None:
    model = BiologicalAgeModel().fit([[1.0], [2.0], [3.0], [4.0]], [10.0, 20.0, 30.0, 40.0])
    metrics = model.evaluate([[1.5], [2.5]], [15.0, 25.0])
    assert metrics.mae < 1e-8
    assert metrics.r_squared > 0.99


def test_kaplan_meier_handles_censoring() -> None:
    points = kaplan_meier([1, 2, 3], [True, False, True])
    assert points[-1].survival == 0.0


def test_pathway_enrichment_and_omics_join() -> None:
    result = enrich_gene_set({"A", "B"}, {"pathway": {"A", "B", "C"}}, {"A", "B", "C", "D"})
    assert result[0].overlap == 2
    joined = integrate_samples(
        [
            MultiOmicsSample("S1", "P1", OmicsLayer.GENOMICS, {"A": 1.0}),
            MultiOmicsSample("S1", "P1", OmicsLayer.TRANSCRIPTOMICS, {"B": None}),
        ]
    )
    assert joined["S1"]["genomics"]["A"] == 1.0
    assert joined["S1"]["transcriptomics"]["B"] is None


def test_pathway_enrichment_uses_full_valid_family_for_bh_adjustment() -> None:
    results = enrich_gene_set(
        {"A", "B"},
        {
            "direct": {"A", "B"},
            "partial": {"A", "C"},
            "no_observed_overlap": {"E", "F"},
            "outside_universe": {"X", "Y"},
        },
        {"A", "B", "C", "D", "E", "F"},
    )

    assert [result.pathway for result in results] == ["direct", "partial"]
    assert results[0].p_value == 1 / 15
    assert results[0].adjusted_p_value == 0.2
    assert [result.adjusted_p_value for result in results] == sorted(
        result.adjusted_p_value for result in results
    )


def test_pathway_enrichment_rejects_genes_outside_universe() -> None:
    try:
        enrich_gene_set({"A", "X"}, {"pathway": {"A"}}, {"A", "B"})
    except ValueError as exc:
        assert "genes must be non-empty" in str(exc)
    else:
        raise AssertionError("Expected genes outside universe to be rejected")


def test_multi_omics_rejects_duplicate_sample_layer_pairs() -> None:
    samples = [
        MultiOmicsSample("S1", "P1", OmicsLayer.GENOMICS, {"A": 1.0}),
        MultiOmicsSample("S1", "P1", OmicsLayer.GENOMICS, {"A": 2.0}),
    ]

    try:
        integrate_samples(samples)
    except ValueError as exc:
        assert "duplicate sample_id and layer" in str(exc)
    else:
        raise AssertionError("Expected duplicate sample/layer pairs to be rejected")


def test_multi_omics_rejects_inconsistent_participant_mapping() -> None:
    samples = [
        MultiOmicsSample("S1", "P1", OmicsLayer.GENOMICS, {"A": 1.0}),
        MultiOmicsSample("S1", "P2", OmicsLayer.TRANSCRIPTOMICS, {"B": 2.0}),
    ]

    try:
        integrate_samples(samples)
    except ValueError as exc:
        assert "one participant_id" in str(exc)
    else:
        raise AssertionError("Expected inconsistent sample participant mapping to fail")
