import logging
from pathlib import Path

import click

from . import reports
from .config import PERSIST_PATH
from .quotes import generate_quotes_csv
from .sources import ingest_sources_as_df

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


@cli.command(name="download-quotes")
def quotes_cmd():
    generate_quotes_csv()


if __name__ == "__main__":
    cli()
