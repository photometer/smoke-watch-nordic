"""Backfill: run the observations pipeline for every day of an archive period."""

from datetime import date

from prefect import flow, get_run_logger

from smoke_watch.dates import day_range
from smoke_watch.flows.daily import daily_pipeline


@flow
def backfill(start: date, end: date, domain_name: str | None = None) -> None:
    """Process every day from start to end (both included), e.g. 2018-06-01 to 2018-08-31.

    Days run one after another; downloads inside each day run in parallel. A failed day is
    logged and skipped, and the backfill is marked failed at the end with the list of days
    to rerun.
    """
    logger = get_run_logger()
    days = list(day_range(start, end))
    logger.info("Backfill of %d day(s): %s to %s", len(days), start, end)

    failed_days: list[date] = []
    for day in days:
        state = daily_pipeline(day=day, domain_name=domain_name, return_state=True)
        if state.is_failed():
            logger.warning("Day %s failed", day)
            failed_days.append(day)

    if failed_days:
        raise RuntimeError(f"Failed days: {', '.join(str(d) for d in failed_days)}")
