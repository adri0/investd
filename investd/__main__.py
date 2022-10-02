import logging
from pathlib import Path

import click

from .source import ingest_sources

log = logging.getLogger("investd")


@click.group()
def investd():
    pass


@click.command(name="ingest-sources")
@click.option("--output", default="data/transactions/tx.csv", help="Output path")
def ingest_sources_cli(output: Path):
    df_tx = ingest_sources()
    log.info(f"Writing {output}")
    df_tx.to_csv(output, index=False)


investd.add_command(ingest_sources_cli)


if __name__ == "__main__":
    investd()
    log.info("Finished!")
