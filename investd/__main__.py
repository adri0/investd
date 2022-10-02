import logging
import sys
from pathlib import Path

import click

from .source import load_txs_from_source

log = logging.getLogger("investd")


@click.group()
def investd():
    pass


@click.command()
@click.option('--output', default="data/transactions/tx.csv", help="Output path")
def load_sources(output: Path):
    df_tx = load_txs_from_source()
    log.info(f"Writing {output}")
    df_tx.to_csv(output, index=False)

investd.add_command(load_sources)


if __name__ == "__main__":
    investd()
