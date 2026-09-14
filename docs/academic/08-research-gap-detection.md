# A08 — Transparent research-gap detection

**Question.** Can a gap detector prioritize reading without pretending to prove absence of evidence?

The detector emits hypotheses based on observed coverage: translational gaps, missing replication, source concentration, validation gaps, small samples, and explicitly outdated records. Each signal carries supporting identifiers and a confidence that reflects rule activation, not truth probability.

```mermaid
flowchart TD
  TOPIC[Topic query] --> COVER[Coverage map]
  COVER --> TRANS[Translation rule]
  COVER --> REPL[Replication rule]
  COVER --> VALID[Validation rule]
  COVER --> SAMPLE[Sample-size rule]
  TRANS --> REPORT[Gap report + evidence IDs]
  REPL --> REPORT
  VALID --> REPORT
  SAMPLE --> REPORT
```

**Reproducibility checks.** Version rules, keep thresholds in code, test boundary cases, and require a reviewer to interpret a gap.
