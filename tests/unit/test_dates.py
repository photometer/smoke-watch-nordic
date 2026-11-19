from datetime import date, timedelta

import pytest

from smoke_watch.dates import day_range, resolve_day

TODAY = date(2026, 11, 18)


def test_no_day_means_yesterday() -> None:
    assert resolve_day(None, today=TODAY) == date(2026, 11, 17)


def test_archive_day_is_kept() -> None:
    assert resolve_day(date(2018, 7, 21), today=TODAY) == date(2018, 7, 21)


@pytest.mark.parametrize("day", [TODAY, TODAY + timedelta(days=1)])
def test_today_and_future_are_rejected(day: date) -> None:
    with pytest.raises(ValueError, match="only finished days"):
        resolve_day(day, today=TODAY)


def test_day_range_includes_both_ends() -> None:
    days = list(day_range(date(2018, 7, 30), date(2018, 8, 2)))
    assert days == [date(2018, 7, 30), date(2018, 7, 31), date(2018, 8, 1), date(2018, 8, 2)]


def test_day_range_single_day() -> None:
    assert list(day_range(date(2018, 7, 21), date(2018, 7, 21))) == [date(2018, 7, 21)]


def test_day_range_rejects_reversed_period() -> None:
    with pytest.raises(ValueError, match="before start"):
        list(day_range(date(2018, 8, 1), date(2018, 7, 1)))
