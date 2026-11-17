import sqlite3

import pytest

from pdf_document_search.__main__ import check_fts5
from pdf_document_search.config import Config, load_config


def test_actual_fts5_matching():
    assert check_fts5() == sqlite3.sqlite_version


def test_defaults_require_no_optional_services():
    config = load_config()
    assert config == Config()
    assert not config.ocr_enabled
    assert not config.semantic_enabled


def test_relative_data_path_uses_config_directory(tmp_path, monkeypatch):
    folder = tmp_path / "settings"
    folder.mkdir()
    path = folder / "local.toml"
    path.write_text('data_dir = "private"\nhost = "::1"\n', encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    config = load_config(path)
    assert config.data_dir == folder / "private"
    assert not config.data_dir.exists()


@pytest.mark.parametrize("value", [
    'host = "0.0.0.0"', 'host = "example.com"', 'port = true', 'port = 0',
    'port = 65536', 'ocr_enabled = "yes"', 'semantic_enabled = 1',
    'data_dir = ""', 'extra = true',
])
def test_invalid_config_is_rejected(tmp_path, value):
    path = tmp_path / "local.toml"
    path.write_text(value, encoding="utf-8")
    with pytest.raises(ValueError):
        load_config(path)
