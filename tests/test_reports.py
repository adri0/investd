from pathlib import Path

from investd.reports import generate_report


def test_generate_overview_report(cleanup_reports):
    report_path = Path("sample_data/reports/overview.html")
    assert not report_path.exists()
    generate_report(Path("investd/reports/overview.py"))
    assert report_path.exists()
