# OpenLongevity 🧬

Open-source computational infrastructure for understanding, measuring, mapping, and modeling biological aging.

[![CI](https://github.com/example/openlongevity/actions/workflows/ci.yml/badge.svg)](https://github.com/example/openlongevity/actions)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

OpenLongevity connects literature, biomarkers, multi-omics metadata, clinical-trial records, and mechanistic relationships into a provenance-preserving research workspace. The initial release is a lightweight, dependency-conscious foundation that can grow toward public scientific APIs and larger data stores.

> Research use only. Not medical advice. OpenLongevity does not diagnose, prevent, treat, or cure disease and does not establish that any intervention extends human lifespan.

## What is included

- Evidence records with study design, provenance, uncertainty, replication, and retraction status.
- A transparent A–G evidence hierarchy that keeps preclinical and human findings distinct.
- A research-gap detector for translational, replication, and source-concentration signals.
- A small graph abstraction for gene, pathway, mechanism, biomarker, intervention, and study links.
- Optional FastAPI routes at `/api/v1/health` and `/api/v1/evidence`.
- A local CLI and synthetic fixtures clearly marked as non-scientific examples.

## Research pipeline

```mermaid
flowchart LR
    A[Scientific sources] --> B[Ingestion]
    B --> C[Normalization]
    C --> D[Evidence records]
    D --> E[Classification]
    E --> F[Knowledge graph]
    F --> G[Research dashboard]
```

## Evidence levels

`A` systematic review/meta-analysis, `B` randomized controlled human study, `C` clinical or prospective evidence, `D` observational human evidence, `E` animal evidence, `F` in-vitro evidence, `G` computational hypothesis. A retracted source remains visible for provenance but is excluded from active summaries.

## Quickstart

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -e ".[dev,api]"
pytest
openlongevity evidence "cellular senescence"
uvicorn 'openlongevity.api:create_app' --factory --reload
```

Synthetic records are for software demonstrations only; they are not evidence for a scientific conclusion.

## Repository structure

```text
src/openlongevity/   typed domain models, evidence engine, graph, API, CLI
tests/                behavior-focused unit tests
docs/                 architecture, security, and research notes
schemas/              data contracts
examples/             synthetic example records
infrastructure/       container and deployment templates
```

## Reproducibility and governance

Every imported record should retain its source identifier, retrieval date, licensing information, and transformation history. AI-generated interpretations are stored separately from source evidence and require human review. See [DATA_GOVERNANCE.md](DATA_GOVERNANCE.md), [REPRODUCIBILITY.md](REPRODUCIBILITY.md), and [SECURITY.md](SECURITY.md).

## Contributing and citation

Please read [CONTRIBUTING.md](CONTRIBUTING.md) and include provenance for scientific changes. Cite the project using [CITATION.cff](CITATION.cff). Project ownership and attribution are documented in [AUTHORS.md](AUTHORS.md).
