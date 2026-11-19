import pytest

from smoke_watch.domain import BBox

BOX = BBox(west=2.0, south=54.0, east=32.0, north=72.0)


def test_cds_area_is_north_west_south_east() -> None:
    assert BOX.cds_area() == [72.0, 2.0, 54.0, 32.0]


def test_firms_area_is_west_south_east_north() -> None:
    assert BOX.firms_area() == "2.0,54.0,32.0,72.0"


def test_stac_bbox_is_west_south_east_north() -> None:
    assert BOX.stac_bbox() == [2.0, 54.0, 32.0, 72.0]


def test_inverted_box_is_rejected() -> None:
    with pytest.raises(ValueError):
        BBox(west=32.0, south=54.0, east=2.0, north=72.0)
