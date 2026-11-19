from datetime import date

from smoke_watch.storage.paths import processed_key, raw_prefix


def test_processed_key_is_partitioned_by_date() -> None:
    key = processed_key("nordic", "aod", date(2018, 7, 21))
    assert key == "processed/nordic/aod/2018/07/21/aod_20180721.tif"


def test_raw_prefix_ends_with_slash() -> None:
    assert raw_prefix("nordic", "firms", date(2018, 7, 1)).endswith("/2018/07/01/")
