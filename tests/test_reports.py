from pathlib import Path

from investd.reports import generate_report


def test_generate_overview_report(cleanup_reports, path_resources):
    generated_report_path = path_resources / "data/reports/overview.html"
    assert not generated_report_path.exists()
    generate_report(Path("investd/reports/overview.py"))
    assert generated_report_path.exists()
