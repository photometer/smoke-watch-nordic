"""Date handling shared by the flows. All dates are UTC days, like the products themselves."""

from collections.abc import Iterator
from datetime import UTC, date, datetime, timedelta


def utc_today() -> date:
    return datetime.now(UTC).date()


def resolve_day(day: date | None, today: date | None = None) -> date:
    """Return the day to process: the given one, or yesterday (UTC) when none is given."""
    today = today or utc_today()
    if day is None:
        return today - timedelta(days=1)
    if day >= today:
        raise ValueError(f"Cannot process {day}: only finished days before {today} (UTC) exist")
    return day


def day_range(start: date, end: date) -> Iterator[date]:
    """Every day from start to end, both included."""
    if end < start:
        raise ValueError(f"End {end} is before start {start}")
    for offset in range((end - start).days + 1):
        yield start + timedelta(days=offset)
