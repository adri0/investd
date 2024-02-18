from pathlib import Path

import pytest
from click.testing import CliRunner
from pytest import MonkeyPatch

import investd
from investd.__main__ import cli
from investd.exceptions import NoTransactions


@pytest.fixture
def empty_data_dir(monkeypatch: MonkeyPatch, tmp_path: Path) -> Path:
    monkeypatch.setattr(investd.config, "INVESTD_DATA", tmp_path)
    for conf in ["PERSIST", "SOURCES", "REPORTS"]:
        monkeypatch.setattr(investd.config, f"INVESTD_{conf}", tmp_path / conf.lower())
    return tmp_path


def test_new_data_dir(empty_data_dir: Path) -> None:
    result = CliRunner().invoke(cli, ["report"])
    assert isinstance(result.exception, NoTransactions)
