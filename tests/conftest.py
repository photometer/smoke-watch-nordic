from pathlib import Path

import pytest
from pydantic import SecretStr

from smoke_watch.config import Settings


@pytest.fixture(autouse=True)
def _no_env_selection(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tests never read .env.<env> files, even if SMOKE_ENV is set in the shell."""
    monkeypatch.delenv("SMOKE_ENV", raising=False)


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    """Settings with test values only; nothing comes from the environment or files."""
    return Settings(
        database_url="postgresql+psycopg://test:test@localhost:5432/test",
        s3_endpoint_url="http://s3.test",
        firms_map_key=SecretStr("test-firms-key"),
        cdse_client_id="test-client",
        cdse_secret=SecretStr("test-secret"),
        data_dir=tmp_path,
    )
