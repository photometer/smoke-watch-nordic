"""Build STAC items for processed products."""

from datetime import date
from typing import Any

from smoke_watch.domain import Domain


def build_item(product: str, day: date, domain: Domain, asset_href: str) -> dict[str, Any]:
    """Return a STAC item for one product on one day."""
    # TODO: use pystac.Item with projection, raster, file and processing extensions
    raise NotImplementedError
