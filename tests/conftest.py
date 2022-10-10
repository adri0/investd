from pathlib import Path

import pytest


@pytest.fixture
def cleanup_reports():
    yield
    for path in Path("sample_data/reports").glob("*.html"):
        path.unlink()


@pytest.fixture
def path_revolut_csv() -> Path:
    return Path("tests/resources/data/sources/revolut-stocks-statement.csv")
