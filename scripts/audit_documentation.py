"""Audit tracked Markdown without counting code as academic prose.

Project author: CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent.
This structural check does not certify academic quality or Mermaid syntax.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from hashlib import sha256
from pathlib import Path
from urllib.parse import unquote, urlsplit

AUTHOR = "CIPRIAN ȘTEFAN PLEȘCA — cercetător român independent"


def prose_and_diagrams(body: str) -> tuple[str, int, bool]:
    """Remove fenced code, including Mermaid, and detect unclosed fences."""
    prose: list[str] = []
    fence: str | None = None
    diagrams = 0
    for line in body.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, language = match.groups()
            if fence is None:
                fence = marker
                diagrams += int(language.strip().lower() == "mermaid")
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not language.strip():
                fence = None
            continue
        if fence is None:
            prose.append(line)
    return "\n".join(prose), diagrams, fence is not None


def inspect(root: Path, name: str, minimum: int) -> dict[str, object]:
    path = root / name
    body = path.read_text(encoding="utf-8-sig")
    prose, diagrams, unclosed = prose_and_diagrams(body)
    broken: list[str] = []
    # Check file targets of inline Markdown links/images and HTML src/href.
    # Reference-style links and fragments require a separate renderer check.
    targets = re.findall(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", prose)
    targets += re.findall(r'''(?:src|href)=["']([^"']+)["']''', prose)
    for target in targets:
        target = target.strip()
        target = target[1:target.index(">")] if target.startswith("<") else target.split()[0]
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        base = root if parsed.path.startswith("/") else path.parent
        destination = base / unquote(parsed.path.lstrip("/"))
        if not destination.exists():
            broken.append(target)
    prose = re.sub(r"<!--.*?-->", " ", prose, flags=re.S)
    prose = re.sub(r"<[^>]+>", " ", prose)
    prose = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", prose)
    prose = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", prose)
    prose = re.sub(r"`[^`]*`", " ", prose)
    prose = re.sub(r"https?://\S+", " ", prose)
    words = len(re.findall(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*", prose, re.UNICODE))
    issues: list[str] = []
    if words < minimum:
        issues.append("below_word_threshold")
    if AUTHOR not in prose:
        issues.append("missing_author_attribution")
    if broken:
        issues.append("broken_local_targets")
    if unclosed:
        issues.append("unclosed_code_fence")
    if name.startswith("docs/academic/") and name != "docs/academic/README.md" and not diagrams:
        issues.append("missing_academic_diagram")
    return {
        "path": name,
        "normalized_text_sha256": sha256(body.encode("utf-8")).hexdigest(),
        "prose_words": words,
        "mermaid_blocks": diagrams,
        "broken_local_targets": sorted(set(broken)),
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--minimum", type=int, default=1000)
    parser.add_argument("--json", action="store_true", help="Print the complete inventory as JSON")
    args = parser.parse_args()
    root = args.root.resolve()
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md"],
        cwd=root, check=True, capture_output=True,
    )
    names = sorted(name for name in result.stdout.decode("utf-8").split("\0") if name)
    rows = [inspect(root, name, args.minimum) for name in names]
    failures = sum(bool(row["issues"]) for row in rows)
    report = {
        "minimum_prose_words": args.minimum,
        "scope": "All tracked Markdown; excludes generated or untracked files and machine metadata",
        "limitations": (
            "Word count is not quality review; Mermaid syntax and URL fragments unchecked"
        ),
        "documents": len(rows),
        "documents_with_issues": failures,
        "results": rows,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=True, indent=2))
    else:
        for row in rows:
            print(f"{row['prose_words']:5} {row['path']}: {', '.join(row['issues']) or 'PASS'}")
        print(f"{failures}/{len(rows)} documents need work; minimum {args.minimum} prose words.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
