"""PostGIS access: engine creation and upserts."""

from functools import cache

from sqlalchemy import Engine, create_engine

from smoke_watch.config import get_settings


@cache
def get_engine() -> Engine:
    return create_engine(get_settings().database_url, pool_pre_ping=True)
