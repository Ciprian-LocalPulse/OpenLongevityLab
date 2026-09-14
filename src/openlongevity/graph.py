"""Small in-memory graph abstraction suitable for demos and API fixtures."""

from collections import defaultdict


class EvidenceGraph:
    def __init__(self) -> None:
        self._edges: dict[str, set[tuple[str, str]]] = defaultdict(set)

    def add_edge(self, subject: str, relation: str, object_: str) -> None:
        if not all(value.strip() for value in (subject, relation, object_)):
            raise ValueError("graph nodes and relation must not be empty")
        self._edges[subject].add((relation, object_))

    def neighbors(self, subject: str) -> list[dict[str, str]]:
        return [{"relation": relation, "object": object_} for relation, object_ in sorted(self._edges.get(subject, set()))]

    def as_dict(self) -> dict[str, list[dict[str, str]]]:
        return {subject: self.neighbors(subject) for subject in sorted(self._edges)}
