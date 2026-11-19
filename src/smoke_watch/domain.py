from dataclasses import dataclass


@dataclass(frozen=True)
class BBox:
    """Bounding box in EPSG:4326 degrees."""

    west: float
    south: float
    east: float
    north: float

    def __post_init__(self) -> None:
        if not (self.west < self.east and self.south < self.north):
            raise ValueError(f"Invalid bounding box: {self}")

    def cds_area(self) -> list[float]:
        # CDS and ADS expect [north, west, south, east]
        return [self.north, self.west, self.south, self.east]

    def firms_area(self) -> str:
        # FIRMS area API expects "west,south,east,north"
        return f"{self.west},{self.south},{self.east},{self.north}"

    def stac_bbox(self) -> list[float]:
        # earthaccess and STAC API format
        return [self.west, self.south, self.east, self.north]

    def wkt(self) -> str:
        # CDSE OData API format
        w, s, e, n = self.west, self.south, self.east, self.north
        return f"POLYGON(({w} {s},{e} {s},{e} {n},{w} {n},{w} {s}))"


@dataclass(frozen=True)
class Domain:
    name: str
    bbox: BBox
    crs: str
    resolution_m: int
    region_key: str
