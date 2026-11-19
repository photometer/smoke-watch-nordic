"""CAMS global composition forecast (AOD, PM2.5) from the Atmosphere Data Store, GRIB."""

from datetime import date
from pathlib import Path

from smoke_watch.domain import Domain


def fetch_cams_forecast(domain: Domain, run_date: date, out_dir: Path) -> Path:
    """Download the forecast for the domain. cdsapi expects area as domain.bbox.cds_area()."""
    raise NotImplementedError
