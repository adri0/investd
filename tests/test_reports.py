from investd.config import INVESTD_REPORTS
from investd.reports import generate_report


def test_generate_overview_report(cleanup_reports):
    assert not list(INVESTD_REPORTS.glob("*.html"))
    report_path = generate_report("overview")
    assert report_path in list(INVESTD_REPORTS.glob("*.html"))
