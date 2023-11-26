import logging
from dataclasses import fields
from itertools import chain
from pathlib import Path
from typing import Optional, Type

import pandas as pd

from investd import config
from investd.sources import bonds, bossa, revolut_stocks, xtb
from investd.sources.base import SourceBase
from investd.transaction import Transaction

log = logging.getLogger(__name__)

sources: list[Type[SourceBase]] = [
    xtb.XTB,
    revolut_stocks.RevolutStocks,
    bonds.Bonds,
    bossa.Bossa,
]


def ingest_all() -> pd.DataFrame:
    df_tx = pd.DataFrame(
        list(chain.from_iterable(Source().load_transactions() for Source in sources)),
        columns=[field.name for field in fields(Transaction)],
    )
    df_tx.sort_values(by="timestamp", ascending=True, inplace=True)
    return df_tx


def ingest_to_path(path_output: Optional[Path] = None) -> None:
    path_output = path_output or (config.INVESTD_PERSIST / "transactions.csv")
    df_tx = ingest_all()
    log.info(f"Writing {path_output}")
    path_output.parent.mkdir(exist_ok=True, parents=True)
    df_tx.to_csv(path_output, index=False)
