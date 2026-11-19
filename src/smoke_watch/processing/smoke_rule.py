"""Rule that flags a smoke day for a region."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    """Signals for one region on one day; None means the source was unavailable."""

    aod_p90: float | None
    co_anomaly: float | None
    upwind_fire_count: int | None
    pm25_max: float | None


@dataclass(frozen=True)
class Thresholds:
    aod_p90: float
    co_anomaly: float
    upwind_fire_count: int
    pm25_max: float


def is_smoke_day(evidence: Evidence, thresholds: Thresholds) -> bool:
    """Decide whether the region was affected by smoke."""
    raise NotImplementedError
