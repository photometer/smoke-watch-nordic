"""NILU air quality stations and hourly PM2.5 (JSON API)."""

from datetime import date

import pandas as pd


def fetch_stations() -> pd.DataFrame:
    """Station metadata: id, name, lat, lon."""
    raise NotImplementedError


def fetch_observations(day: date, component: str = "PM2.5") -> pd.DataFrame:
    """Hourly observations for all stations on the given day."""
    raise NotImplementedError
