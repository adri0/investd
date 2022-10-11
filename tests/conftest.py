from pathlib import Path

import pytest

from investd.config import SOURCE_BASE_PATH


@pytest.fixture
def path_resources() -> Path:
    return Path(__file__).parent / "resources"


@pytest.fixture
def cleanup_reports(path_resources):
    yield
    for path in (path_resources / "data/reports").glob("*.html"):
        path.unlink()


@pytest.fixture
def path_revolut_csv() -> Path:
    return SOURCE_BASE_PATH / "revolut_stocks/revolut-stocks-statement.csv"


@pytest.fixture
def path_xtb_xlsx() -> Path:
    return SOURCE_BASE_PATH / "xtb/xtb-statement.xlsx"
