# OpenLongevity 🧬

Open-source computational infrastructure for understanding, measuring, mapping, and modeling biological aging.

![OpenLongevity — open science for a healthier tomorrow](assets/OPENLONGEVITY.png)

[![CI](https://github.com/Ciprian-LocalPulse/OpenLongevityLab/actions/workflows/ci.yml/badge.svg)](https://github.com/Ciprian-LocalPulse/OpenLongevityLab/actions)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

OpenLongevity connects literature, biomarkers, multi-omics metadata, clinical-trial records, and mechanistic relationships into a provenance-preserving research workspace. Version 0.2.0 is an MVP foundation with live read-only source adapters, a PostgreSQL persistence path, transparent analysis modules, and a reviewable dashboard.

> Research use only. Not medical advice. OpenLongevity does not diagnose, prevent, treat, or cure disease and does not establish that any intervention extends human lifespan.

## Core capabilities

- Evidence records with study design, provenance, uncertainty, replication, and retraction status.
- A transparent A–G hierarchy distinguishing in-vitro, animal, observational human, clinical, RCT, review, and computational evidence.
- Research-gap signals for translational, replication, and source-concentration patterns.
- A graph abstraction for gene, pathway, mechanism, biomarker, intervention, and study links.
- Optional FastAPI routes and a typed TypeScript dashboard shell.
- Read-only adapters for PubMed, Europe PMC, OpenAlex, Crossref, and ClinicalTrials.gov with provenance on every normalized record.
- PostgreSQL-ready repositories, evidence scoring, contradiction surfacing, pathway enrichment, survival curves, biological-age baselines, and multi-omics joins.

## Research pipeline

```mermaid
flowchart LR
    A[Scientific sources] --> B[Read-only adapters]
    B --> C[Normalization + provenance]
    C --> D[Evidence records]
    D --> E[Review + scoring]
    E --> F[Knowledge graph and gap signals]
    F --> G[Research dashboard]
```

## Quickstart

```bash
python -m venv .venv
pip install -e ".[dev,api]"
pytest
    openlongevity evidence "cellular senescence"
uvicorn 'openlongevity.api:create_app' --factory --reload
```

Synthetic records are software fixtures only and are not scientific conclusions. See [limitations](docs/research/LIMITATIONS.md), [data sources](docs/data/DATA_SOURCES.md), and the [v0.2.0 release notes](docs/releases/v0.2.0.md).

## Repository structure

```text
src/openlongevity/   typed scientific core, API, and CLI
biomarkers/          biomarker catalog and interpretation guardrails
literature/          source adapter contracts
apps/web/             TypeScript dashboard shell
packages/rust/        optional safe performance kernels
sql/                  PostgreSQL schema
docs/                 architecture, evidence, security, and wiki
```

## Author

**Ciprian Ștefan Pleșca** — Founder, Project Creator, Lead Maintainer, and Principal Author. See [AUTHORS.md](AUTHORS.md) and [CITATION.cff](CITATION.cff).

## Governance and contribution

AI-generated interpretations remain separate from source evidence and require review. Every imported record should retain source identifier, retrieval date, license, and transformation history. See [DATA_GOVERNANCE.md](DATA_GOVERNANCE.md), [REPRODUCIBILITY.md](REPRODUCIBILITY.md), [SECURITY.md](SECURITY.md), and [CONTRIBUTING.md](CONTRIBUTING.md).
