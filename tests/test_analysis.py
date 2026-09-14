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
    joined = integrate_samples([MultiOmicsSample("S1", "P1", OmicsLayer.GENOMICS, {"A": 1.0})])
    assert joined["S1"]["genomics"]["A"] == 1.0
