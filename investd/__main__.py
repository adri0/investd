import datetime
import logging
import os
from pathlib import Path
from typing import Optional

import click

from investd import config, quotes, reports, sources
from investd.exceptions import InvestdError
from investd.transaction import TX_FILENAME

APP_NAME = "investd"
log = logging.getLogger(APP_NAME)

HELP_TEXT = f"""{APP_NAME} - A tool for summarizing investments.

How it works: Investd read accounts statements from a INVESTD_SOURCES directory,
process them and write HTML reports to the INVESTD_REPORTS directory.

By default, both INVESTD_SOURCES and INVESTD_REPORTS directories are located in the
INVESTD_DATA dir. Each of these locations can be configured by environment variables.
If INVESTD_DATA environment variable is not provided, a dir named 'investd_data'
at the current working directory will be created and used as such.
"""


cli = click.Group(name=APP_NAME, help=HELP_TEXT)


@cli.command(name="ingest-sources")
@click.option(
    "--output",
    type=click.Path(dir_okay=False, writable=True),
    default=config.INVESTD_PERSIST / TX_FILENAME,
    help="Output path",
)
def ingest_sources_cmd(output: Path) -> None:
    sources.ingest_to_path(output)


@cli.command(name="report")
@click.option(
    "--report",
    default="overview",
    help="Report name",
)
@click.option(
    "--ingest",
    "-i",
    default=True,
    help="Ingests sources before generating report",
    is_flag=True,
)
@click.option(
    "--date",
    "-d",
    default=None,
    help="Show portfolio at a certain date. Use today if not provided.",
)
def report_cmd(report: str, ingest: bool, date: Optional[str]) -> None:
    if ingest:
        sources.ingest_to_path()
    os.environ["REPORT_DATE"] = date or str(datetime.date.today())
    path_output = reports.generate_report(report)
    log.info(f"Report created: {path_output}")
    print(path_output)


@cli.command(
    name="download-quotes",
    help="Download quotes using Yahoo finance API. If start date, symbols not "
    "provided it will look for all symbols in the persisted transactions, "
    "using the earliest transaction as start date and current dateas end date.",
)
@click.option("--start", "-s", default=None, help="Starting date in format YYYY-MM-DD")
@click.option("--end", "-e", default=None, help="End date in format YYYY-MM-DD")
@click.option("--symbols", "-y", default=None, help="Symbols e.g. AAPL,CDR.PL")
def quotes_cmd(
    start: Optional[str], end: Optional[str], symbols: Optional[str]
) -> None:
    quotes.download_quotes_to_csv(
        start_date=datetime.date.fromisoformat(start) if start else None,
        end_date=datetime.date.fromisoformat(end) if end else None,
        symbols=symbols.split(",") if symbols else None,
        include_exchange_rates=True,
    )


def main() -> None:
    config.init_dirs()
    try:
        cli()
    except InvestdError as exc:
        log.error(exc.msg, exc_info=True)
        click.echo(exc.msg)
        exit(1)


if __name__ == "__main__":
    main()
