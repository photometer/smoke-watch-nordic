"""Target grid derived from the domain, shared by every product."""

import math

from smoke_watch.domain import Domain

Bounds = tuple[float, float, float, float]


def snap_bounds(bounds: Bounds, resolution: float) -> Bounds:
    """Expand bounds outward to multiples of resolution so all products share pixel edges."""
    minx, miny, maxx, maxy = bounds
    return (
        math.floor(minx / resolution) * resolution,
        math.floor(miny / resolution) * resolution,
        math.ceil(maxx / resolution) * resolution,
        math.ceil(maxy / resolution) * resolution,
    )


def target_bounds(domain: Domain) -> Bounds:
    """Domain bbox reprojected to the target CRS and snapped to the resolution."""
    from rasterio.warp import transform_bounds

    b = domain.bbox
    projected = transform_bounds(
        "EPSG:4326", domain.crs, b.west, b.south, b.east, b.north, densify_pts=21
    )
    return snap_bounds(projected, domain.resolution_m)
