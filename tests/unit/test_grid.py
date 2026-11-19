from smoke_watch.processing.grid import snap_bounds


def test_snap_bounds_expands_outward() -> None:
    assert snap_bounds((1200.0, -800.0, 9100.0, 4999.0), 5000) == (0, -5000, 10000, 5000)


def test_snap_bounds_keeps_aligned_values() -> None:
    assert snap_bounds((0.0, 0.0, 10000.0, 5000.0), 5000) == (0, 0, 10000, 5000)
