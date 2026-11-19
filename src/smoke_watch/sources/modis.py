"""MODIS MAIAC aerosol optical depth (MCD19A2 v061, HDF4) from NASA Earthdata."""

from datetime import date
from pathlib import Path
from typing import Any

from smoke_watch.domain import Domain

SHORT_NAME = "MCD19A2"
VERSION = "061"


def search_maiac(domain: Domain, start: date, end: date) -> list[Any]:
    """Find MCD19A2 granules covering the domain between start and end (inclusive)."""
    raise NotImplementedError


def download_granules(granules: list[Any], out_dir: Path) -> list[Path]:
    """Download granules to out_dir."""
    raise NotImplementedError
