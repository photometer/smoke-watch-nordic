"""Thin wrapper around the HYSPLIT trajectory model (hyts_std)."""

from datetime import datetime
from pathlib import Path

import pandas as pd


def write_control(
    workdir: Path,
    start: datetime,
    lat: float,
    lon: float,
    heights_m: list[float],
    hours: int,
    meteo_files: list[Path],
    output_name: str = "tdump",
) -> Path:
    """Write a HYSPLIT CONTROL file. Negative `hours` gives back trajectories."""
    raise NotImplementedError


def run_hysplit(workdir: Path, executable: str = "hyts_std") -> Path:
    """Run HYSPLIT in workdir and return the path of the trajectory output."""
    # TODO: subprocess.run([executable], cwd=workdir, check=True, timeout=...)
    raise NotImplementedError


def parse_tdump(path: Path) -> pd.DataFrame:
    """Parse a tdump file into one row per trajectory point."""
    raise NotImplementedError
