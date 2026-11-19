"""Single source of truth for object keys in the data lake."""

from datetime import date


def raw_prefix(domain: str, source: str, day: date) -> str:
    return f"raw/{domain}/{source}/{day:%Y/%m/%d}/"


def quarantine_prefix(domain: str, source: str, day: date) -> str:
    return f"quarantine/{domain}/{source}/{day:%Y/%m/%d}/"


def processed_key(domain: str, product: str, day: date, suffix: str = "tif") -> str:
    return f"processed/{domain}/{product}/{day:%Y/%m/%d}/{product}_{day:%Y%m%d}.{suffix}"


def reference_key(kind: str, name: str, suffix: str = "parquet") -> str:
    return f"reference/{kind}/{name}.{suffix}"
