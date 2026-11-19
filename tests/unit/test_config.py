import os
from pathlib import Path

import pytest
from pydantic import ValidationError

from smoke_watch.config import Settings, load_domain, load_env_files


def test_load_known_domain() -> None:
    domain = load_domain("nordic")
    assert domain.bbox.west < domain.bbox.east
    assert domain.crs == "EPSG:3035"


def test_unknown_domain_lists_known_ones() -> None:
    with pytest.raises(ValueError, match="nordic"):
        load_domain("nordik")


def test_settings_fixture_uses_test_values(settings: Settings, tmp_path: Path) -> None:
    assert settings.data_dir == tmp_path
    assert settings.firms_map_key.get_secret_value() == "test-firms-key"


def test_required_settings_fail_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SMOKE_DATABASE_URL", raising=False)
    with pytest.raises(ValidationError, match="database_url"):
        Settings()  # type: ignore[call-arg]


def test_no_env_selected_loads_nothing(tmp_path: Path) -> None:
    (tmp_path / ".env.dev").write_text("SMOKE_TEST_ONLY=shared\n")
    assert load_env_files(None, tmp_path) == []


def test_env_file_precedence(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / ".env.dev").write_text("SMOKE_A=shared\nSMOKE_B=shared\nSMOKE_C=shared\n")
    (tmp_path / ".env.dev.local").write_text("SMOKE_B=local\nSMOKE_C=local\n")
    for name in ("SMOKE_A", "SMOKE_B"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("SMOKE_C", "real")

    load_env_files("dev", tmp_path)

    assert os.environ["SMOKE_A"] == "shared"
    assert os.environ["SMOKE_B"] == "local"
    assert os.environ["SMOKE_C"] == "real"
    for name in ("SMOKE_A", "SMOKE_B"):
        monkeypatch.delenv(name)  # load_dotenv writes os.environ directly; clean up


def test_unknown_env_file_is_an_error(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="SMOKE_ENV='deb'"):
        load_env_files("deb", tmp_path)
