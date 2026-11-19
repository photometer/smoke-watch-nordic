"""Write rasters as Cloud Optimized GeoTIFF."""

from pathlib import Path

import rioxarray  # noqa: F401
import xarray as xr


def write_cog(da: xr.DataArray, path: Path) -> Path:
    """Write a georeferenced DataArray as COG with internal overviews."""
    path.parent.mkdir(parents=True, exist_ok=True)
    da.rio.to_raster(path, driver="COG", compress="DEFLATE")
    return path
