"""ECMWF Open Data IFS forecast (GRIB2). Global fields: crop to the domain after download."""

from datetime import date
from pathlib import Path


def fetch_ifs_wind(run_date: date, out_dir: Path, levels_hpa: tuple[int, ...] = (850,)) -> Path:
    """Download u/v wind for the given run (ecmwf-opendata client)."""
    raise NotImplementedError
