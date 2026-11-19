"""Runtime settings and domain loading."""

import os
from functools import cache
from importlib.resources import files
from pathlib import Path

import yaml
from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from smoke_watch.domain import BBox, Domain


class Settings(BaseSettings):
    """Settings read from SMOKE_* environment variables.

    Fields without a default differ between environments and must always be set.
    """

    model_config = SettingsConfigDict(env_prefix="SMOKE_", extra="ignore")

    # Same in every environment
    domain: str = "nordic"
    data_dir: Path = Path("data")
    s3_bucket: str = "smoke-data"

    # Environment-specific
    database_url: str
    s3_endpoint_url: str
    firms_map_key: SecretStr
    cdse_client_id: str
    cdse_secret: SecretStr


def load_env_files(env: str | None = None, base_dir: Path | None = None) -> list[Path]:
    """Load .env.<env>.local and .env.<env> into os.environ for the selected environment.

    The environment name comes from SMOKE_ENV (for example "dev"). When it is not set,
    nothing is loaded: production and tests take values from the real environment only.
    Precedence: real environment variables > .env.<env>.local > .env.<env>.
    Values go into os.environ, so libraries such as boto3, cdsapi and earthaccess see them too.
    """
    env = env if env is not None else os.environ.get("SMOKE_ENV")
    if not env:
        return []

    base_dir = base_dir or Path.cwd()
    shared = base_dir / f".env.{env}"
    if not shared.is_file():
        raise FileNotFoundError(f"SMOKE_ENV={env!r} but {shared} does not exist")

    loaded = []
    for path in (base_dir / f".env.{env}.local", shared):  # first loaded wins (no override)
        if path.is_file():
            load_dotenv(path, override=False)
            loaded.append(path)
    return loaded


@cache
def get_settings() -> Settings:
    load_env_files()
    return Settings()  # type: ignore[call-arg]  # required fields come from the environment


@cache
def load_domain(name: str) -> Domain:
    """Load a domain definition from the packaged domains.yaml."""
    text = files("smoke_watch").joinpath("domains.yaml").read_text(encoding="utf-8")
    all_domains = yaml.safe_load(text)

    if name not in all_domains:
        known = ", ".join(sorted(all_domains))
        raise ValueError(f"Unknown domain '{name}'. Known domains: {known}")

    raw = all_domains[name]
    west, south, east, north = raw["bbox"]
    return Domain(
        name=name,
        bbox=BBox(west, south, east, north),
        crs=raw["crs"],
        resolution_m=int(raw["resolution_m"]),
        region_key=raw["region_key"],
    )
