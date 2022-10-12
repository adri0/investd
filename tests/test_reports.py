from investd.config import REPORTS_PATH
from investd.reports import generate_report


def test_generate_overview_report(cleanup_reports):
    assert not list(REPORTS_PATH.glob("*.html"))
    report_path = generate_report("overview")
    assert report_path in list(REPORTS_PATH.glob("*.html"))
