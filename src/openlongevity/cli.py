"""Command-line entry point for deterministic local exploration."""

import argparse

from .evidence import EvidenceEngine
from .models import EvidenceRecord, StudyType


def main() -> None:
    parser = argparse.ArgumentParser(prog="openlongevity", description="Evidence-first aging research tooling")
    parser.add_argument("command", choices=["evidence", "search"])
    parser.add_argument("topic")
    args = parser.parse_args()
    record = EvidenceRecord("SYN-001", args.topic, StudyType.COMPUTATIONAL, "n/a", "research signal", "synthetic fixture", confidence=0.2)
    print(f"{args.command}: {args.topic}\nEvidence level: {EvidenceEngine().grade(record).value}\nResearch use only. Not medical advice.")
