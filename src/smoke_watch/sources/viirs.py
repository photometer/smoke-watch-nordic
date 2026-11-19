"""VIIRS Deep Blue aerosol (AERDB_L2_VIIRS_NOAA20, NetCDF4 swath), MODIS successor."""

from datetime import date
from pathlib import Path
from typing import Any

from smoke_watch.domain import Domain

SHORT_NAME = "AERDB_L2_VIIRS_NOAA20"


def search_aerdb(domain: Domain, start: date, end: date) -> list[Any]:
    """Find VIIRS Deep Blue granules over the domain."""
    raise NotImplementedError


def download_granules(granules: list[Any], out_dir: Path) -> list[Path]:
    raise NotImplementedError
