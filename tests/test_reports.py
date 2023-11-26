from investd import config
from investd.reports import generate_report


def test_generate_overview_report(setup_reports: None) -> None:
    assert not list(config.INVESTD_REPORTS.glob("*.html"))
    report_path = generate_report("overview")
    assert report_path in list(config.INVESTD_REPORTS.glob("*.html"))
