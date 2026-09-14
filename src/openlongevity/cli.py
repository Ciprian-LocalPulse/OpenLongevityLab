"""Command-line entry point."""
import argparse
from .evidence import EvidenceEngine
from .models import EvidenceRecord, StudyType
def main() -> None:
    parser = argparse.ArgumentParser(prog="openlongevity")
    parser.add_argument("command", choices=["evidence", "search", "biomarker", "gaps", "graph"])
    parser.add_argument("topic")
    args = parser.parse_args()
    record = EvidenceRecord("SYN-CLI", args.topic, StudyType.COMPUTATIONAL, "n/a", "research signal", "synthetic fixture", confidence=0.2)
    print(
        f"{args.command}: {args.topic}\n"
        f"Evidence level: {EvidenceEngine().grade(record).value}\n"
        "Research use only. Not medical advice."
    )
