"""NOAA GDAS1 meteorology in ARL format, used as HYSPLIT input."""

from pathlib import Path

ARL_FTP_HOST = "arlftp.arlhq.noaa.gov"
GDAS1_DIR = "archives/gdas1"
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


def gdas1_filenames(year: int, month: int) -> list[str]:
    """GDAS1 archive files are split by week: gdas1.<mon><yy>.w1 ... w5."""
    raise NotImplementedError


def download_gdas1(year: int, month: int, out_dir: Path) -> list[Path]:
    """Download the weekly GDAS1 files for one month. Skips files that already exist."""
    raise NotImplementedError
