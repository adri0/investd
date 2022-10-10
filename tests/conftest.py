from pathlib import Path

import pytest


@pytest.fixture
def cleanup_reports(path_resources):
    yield
    for path in (path_resources / "data/reports").glob("*.html"):
        path.unlink()


@pytest.fixture
def path_revolut_csv(path_resources) -> Path:
    return path_resources / "data/sources/revolut-stocks-statement.csv"


@pytest.fixture
def path_resources() -> Path:
    return Path(__file__).parent / "resources"
