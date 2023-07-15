import logging
import os
from datetime import date
from pathlib import Path
from typing import Optional

import click

from investd import quotes, reports, sources
from investd.config import INVESTD_PERSIST, init_dirs
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
    default=INVESTD_PERSIST / TX_FILENAME,
    help="Output path",
)
def ingest_sources_cmd(output: Path):
    df_tx = sources.ingest_all()
    log.info(f"Writing {output}")
    df_tx.to_csv(output, index=False)


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
def report_cmd(report: str, ingest: bool, date: Optional[str]):
    if ingest:
        df_tx = sources.ingest_all()
        df_tx.to_csv(INVESTD_PERSIST / TX_FILENAME, index=False)
    os.environ["REPORT_DATE"] = date
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
def quotes_cmd(start: Optional[str], end: Optional[str], symbols: Optional[str]):
    quotes.download_quotes_to_csv(
        start_date=date.fromisoformat(start) if start else None,
        end_date=date.fromisoformat(end) if end else None,
        symbols=symbols.split(",") if symbols else None,
        include_exchange_rates=True,
    )


if __name__ == "__main__":
    init_dirs()
    cli()
