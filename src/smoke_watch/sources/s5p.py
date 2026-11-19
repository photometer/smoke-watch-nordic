"""Sentinel-5P TROPOMI CO and aerosol index (L2, NetCDF4 swath) from Copernicus Data Space."""

from datetime import date
from pathlib import Path

from smoke_watch.domain import Domain


def search_s5p(domain: Domain, day: date, product: str = "L2__CO____") -> list[str]:
    """Return product ids intersecting the domain on the given day (use domain.bbox.wkt())."""
    raise NotImplementedError


def download_s5p(product_ids: list[str], out_dir: Path) -> list[Path]:
    raise NotImplementedError
