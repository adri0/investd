import logging
from datetime import date
from pathlib import Path
from typing import Optional

import click

from investd import reports
from investd.config import PERSIST_PATH
from investd.quotes import generate_quotes_csv
from investd.sources import ingest_sources_as_df

app_name = "investd"
log = logging.getLogger(app_name)


cli = click.Group(name=app_name, help="investd - A tool for summarizing investments.")


@cli.command(name="ingest-sources")
@click.option(
    "--output",
    type=click.Path(dir_okay=False, writable=True),
    default=PERSIST_PATH / "tx.csv",
    help="Output path",
)
def ingest_sources_cmd(output: Path):
    df_tx = ingest_sources_as_df()
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
def report_cmd(report: str, ingest: bool):
    if ingest:
        df_tx = ingest_sources_as_df()
        df_tx.to_csv(PERSIST_PATH / "tx.csv", index=False)
    path_output = reports.generate_report(report)
    log.info(f"Report created: {path_output}")


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
    generate_quotes_csv(
        start_date=date.fromisoformat(start) if start else None,
        end_date=date.fromisoformat(end) if end else None,
        symbols=symbols.split(",") if symbols else None,
    )


if __name__ == "__main__":
    cli()
