"""Forecast pipeline: what smoke is expected over the next three days.

Runs only for recent forecast runs: ECMWF Open Data keeps just the last few days, so there is
no backfill here. Archive questions go to the observations pipeline (flows/daily.py).
"""

from datetime import date, timedelta
from pathlib import Path

from prefect import flow, get_run_logger
from prefect.futures import PrefectFuture

from smoke_watch.config import get_settings, load_domain
from smoke_watch.dates import utc_today
from smoke_watch.flows.common import collect_downloads

# from prefect import task
# from smoke_watch.domain import Domain
# from smoke_watch.sources import cams, ecmwf

# How far back ECMWF Open Data still has runs. Check the current retention before relying on it.
OPEN_DATA_RETENTION_DAYS = 4


# @task(retries=2, retry_delay_seconds=600)  # CDS queues requests, so retry rarely
# def download_cams_forecast(domain: Domain, run_date: date, out_dir: Path) -> list[Path]:
#     return [cams.fetch_cams_forecast(domain, run_date, out_dir)]
#
#
# @task(retries=3, retry_delay_seconds=120)
# def download_ifs_wind(run_date: date, out_dir: Path) -> list[Path]:
#     return [ecmwf.fetch_ifs_wind(run_date, out_dir)]


@flow
def forecast_pipeline(run_date: date | None = None, domain_name: str | None = None) -> None:
    """Forecast for one run date (UTC). Leave `run_date` empty for today's run."""
    logger = get_run_logger()
    settings = get_settings()
    domain = load_domain(domain_name or settings.domain)
    today = utc_today()
    run_date = run_date or today
    if not today - timedelta(days=OPEN_DATA_RETENTION_DAYS) <= run_date <= today:
        raise ValueError(
            f"Forecast run {run_date} is outside the last {OPEN_DATA_RETENTION_DAYS} days; "
            "use the observations pipeline for archive dates"
        )
    raw_dir = settings.data_dir / "raw" / domain.name / "forecast" / f"{run_date:%Y%m%d}"
    logger.info("Forecast for %s, run %s, raw files in %s", domain.name, run_date, raw_dir)

    # 1. Start all downloads at once.
    downloads: dict[str, PrefectFuture[list[Path]]] = {
        # "cams": download_cams_forecast.submit(domain, run_date, raw_dir / "cams"),
        # "ifs": download_ifs_wind.submit(run_date, raw_dir / "ifs"),
    }

    # 2. Collect results.
    raw_files, failed = collect_downloads(downloads, logger)

    # 3. Regrid the forecast fields (AOD, PM2.5, wind at 850 hPa) to the domain grid -> COG.
    # 4. Expected smoke per region and day: zonal stats of the forecast AOD/PM2.5.
    # 5. Catalog: STAC items with the forecast run and lead time.
    # TODO: implement once the CAMS and ECMWF readers exist

    if failed:
        raise RuntimeError(f"Sources failed: {', '.join(failed)}")
