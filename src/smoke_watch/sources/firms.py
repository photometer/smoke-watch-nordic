"""NASA FIRMS active fire detections (area API, CSV)."""

from datetime import date
from pathlib import Path

from smoke_watch.domain import Domain


def firms_url(map_key: str, source: str, area: str, day_range: int, day: date) -> str:
    """Build a FIRMS area API URL."""
    raise NotImplementedError


def fetch_firms_csv(
    domain: Domain,
    day: date,
    map_key: str,
    source: str = "MODIS_SP",
    day_range: int = 1,
    timeout_s: float = 60.0,
) -> str:
    """Download fire detections for the domain as CSV text.

    `source` examples: MODIS_SP and VIIRS_SNPP_SP for archive data, *_NRT for recent days.
    """
    raise NotImplementedError


def save_csv(text: str, out_dir: Path, day: date, source: str) -> Path:
    """Write the CSV to disk and return its path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"firms_{source}_{day:%Y%m%d}.csv"
    path.write_text(text, encoding="utf-8")
    return path
