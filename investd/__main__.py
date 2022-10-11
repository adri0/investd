import logging
from pathlib import Path

import click

from . import reports
from .config import PERSIST_PATH
from .sources import ingest_sources_as_df

app_name = "investd"
log = logging.getLogger(app_name)


@click.command(name="ingest-sources")
@click.option(
    "--output",
    type=click.Path(dir_okay=False, writable=True),
    default=PERSIST_PATH / "tx.csv",
    help="Output path",
)
def ingest_sources_cmd(output: Path):
    df_tx = ingest_sources_as_df()
    df_tx.sort_values(by="timestamp", ascending=True, inplace=True)
    log.info(f"Writing {output}")
    df_tx.to_csv(output, index=False)


@click.command(name="report")
@click.option(
    "--report",
    default="overview",
    help="Report name",
)
def report_cmd(report: str):
    reports.generate_report(report)


cli = click.Group(
    name=app_name,
    help="investd - A tool for summarizing investments.",
    commands=[ingest_sources_cmd, report_cmd],
)

if __name__ == "__main__":
    cli()
