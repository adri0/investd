from pathlib import Path

import pytest


@pytest.fixture
def cleanup_reports():
    yield
    for path in Path("sample_data/reports").glob("*.html"):
        path.unlink()
