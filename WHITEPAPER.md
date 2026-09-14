# OpenLongevity: an evidence-first computational foundation for aging research

## Abstract

OpenLongevity is an open-source architecture for connecting heterogeneous aging research into reviewable, reproducible evidence records. It separates source observations from computational interpretation and exposes uncertainty rather than collapsing it into a single claim.

## Motivation and scope

Aging research spans molecular mechanisms, model organisms, observational cohorts, interventions, biomarkers, and clinical trials. These sources use different identifiers, endpoints, and maturity levels. OpenLongevity provides shared models, provenance fields, evidence classification, graph relationships, and research-gap heuristics. It is research infrastructure, not a clinical product.

## Architecture

The platform is organized as ingestion, normalization, evidence extraction, classification, graph storage, and query interfaces. The Python core is intentionally small so that adapters for PubMed, Crossref, OpenAlex, Europe PMC, and ClinicalTrials.gov can be added with their own terms-of-use and rate-limit controls. PostgreSQL and vector or graph backends remain deployment options rather than hard requirements.

## Evidence and translation

The A–G hierarchy records study design maturity. A mouse result may be valuable mechanistic evidence while still leaving a translational gap. Retractions and expressions of concern remain visible for auditability and are prevented from silently improving active confidence summaries.

## Biomarkers and multi-omics

Future adapters can represent epigenomic, transcriptomic, proteomic, metabolomic, genomic, and microbiomic measurements using FAIR-oriented metadata. No single biomarker is treated as a definitive measure of biological age; interpretation should include confounders, calibration, cohort, tissue, and assay limitations.

## Limitations and future work

The current release uses synthetic fixtures and deterministic heuristics. It does not make clinical claims, infer causality, or replace systematic review. Future work includes validated source adapters, entity resolution, richer graph persistence, reproducible notebooks, and independent scientific review.

References should be added only after verification against the original publication or registry record.
