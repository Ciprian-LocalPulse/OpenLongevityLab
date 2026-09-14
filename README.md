# OpenLongevity 🧬

Open-source computational infrastructure for understanding, measuring, mapping, and modeling biological aging.

![OpenLongevity — open science for a healthier tomorrow](assets/OPENLONGEVITY.png)

[![CI](https://github.com/example/openlongevity/actions/workflows/ci.yml/badge.svg)](https://github.com/example/openlongevity/actions)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

OpenLongevity connects literature, biomarkers, multi-omics metadata, clinical-trial records, and mechanistic relationships into a provenance-preserving research workspace. This release is a dependency-conscious foundation ready for public scientific API adapters and larger data stores.

> Research use only. Not medical advice. OpenLongevity does not diagnose, prevent, treat, or cure disease and does not establish that any intervention extends human lifespan.

## Core capabilities

- Evidence records with study design, provenance, uncertainty, replication, and retraction status.
- A transparent A–G hierarchy distinguishing in-vitro, animal, observational human, clinical, RCT, review, and computational evidence.
- Research-gap signals for translational, replication, and source-concentration patterns.
- A graph abstraction for gene, pathway, mechanism, biomarker, intervention, and study links.
- Optional FastAPI routes and a typed TypeScript dashboard shell.

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

## Quickstart

```bash
python -m venv .venv
pip install -e ".[dev,api]"
pytest
openlongevity evidence "cellular senescence"
uvicorn 'openlongevity.api:create_app' --factory --reload
```

Synthetic records are software fixtures only and are not scientific conclusions.

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
