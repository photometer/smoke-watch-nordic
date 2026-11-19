"""Administrative boundaries (fylker) from Shapefile to GeoParquet."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import geopandas as gpd


def shapefile_to_geoparquet(shp_path: Path, out_path: Path, crs: str = "EPSG:4326") -> Path:
    """Read a Shapefile, reproject and save as GeoParquet."""
    raise NotImplementedError


def load_regions(path: Path) -> gpd.GeoDataFrame:
    raise NotImplementedError
