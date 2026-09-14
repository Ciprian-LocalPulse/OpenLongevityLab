"""Dependency-light Kaplan–Meier estimator for demonstrations."""

from dataclasses import dataclass


@dataclass(frozen=True)
class KaplanMeierPoint:
    time: float
    at_risk: int
    events: int
    survival: float


def kaplan_meier(times: list[float], events: list[bool]) -> list[KaplanMeierPoint]:
    """Estimate survival; ``events=False`` denotes right censoring."""
    if not times or len(times) != len(events) or any(time < 0 for time in times):
        raise ValueError("times and events must be aligned and non-negative")
    survival = 1.0
    points: list[KaplanMeierPoint] = []
    for time in sorted(set(times)):
        at_risk = sum(value >= time for value in times)
        deaths = sum(value == time and event for value, event in zip(times, events))
        if at_risk and deaths:
            survival *= 1.0 - deaths / at_risk
        points.append(KaplanMeierPoint(time, at_risk, deaths, round(survival, 6)))
    return points
