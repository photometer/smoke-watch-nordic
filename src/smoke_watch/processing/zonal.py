"""Zonal statistics of rasters over regions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import geopandas as gpd
    import pandas as pd
    import xarray as xr


def zonal_stats(
    raster: xr.DataArray, regions: gpd.GeoDataFrame, region_id: str = "id"
) -> pd.DataFrame:
    """Mean, p90 and valid-pixel fraction per region."""
    raise NotImplementedError
