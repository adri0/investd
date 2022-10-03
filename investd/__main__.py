import logging
from pathlib import Path

import click

from .sources import ingest_sources

app_name = "investd"
log = logging.getLogger(app_name)


@click.command(name="ingest-sources")
@click.option(
    "--output",
    type=click.Path(dir_okay=False, writable=True),
    default="data/transactions/tx.csv",
    help="Output path",
)
def ingest_sources_cmd(output: Path):
    df_tx = ingest_sources()
    log.info(f"Writing {output}")
    df_tx.to_csv(output, index=False)


cli = click.Group(
    name=app_name,
    help="investd - A tool for summarizing investments.",
    commands=[ingest_sources_cmd],
)

if __name__ == "__main__":
    cli()
