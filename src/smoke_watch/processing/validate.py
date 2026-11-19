"""Data checks applied before anything reaches processed/."""

import numpy as np
import xarray as xr


class ValidationError(Exception):
    """Raised when a file fails a check and must go to quarantine."""


def check_value_range(
    da: xr.DataArray, vmin: float, vmax: float, max_bad_fraction: float = 0.0
) -> None:
    """Fail if more than max_bad_fraction of valid values lie outside [vmin, vmax]."""
    values = da.values
    valid = values[np.isfinite(values)]
    if valid.size == 0:
        raise ValidationError(f"{da.name}: no valid values")
    bad_fraction = float(np.mean((valid < vmin) | (valid > vmax)))
    if bad_fraction > max_bad_fraction:
        raise ValidationError(f"{da.name}: {bad_fraction:.1%} of values outside [{vmin}, {vmax}]")


def check_missing_fraction(da: xr.DataArray, max_missing: float) -> None:
    """Fail if the share of missing values is above max_missing."""
    missing = float(np.mean(~np.isfinite(da.values)))
    if missing > max_missing:
        raise ValidationError(f"{da.name}: {missing:.1%} missing, limit {max_missing:.1%}")
