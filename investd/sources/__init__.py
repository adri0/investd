from dataclasses import fields
from itertools import chain
from typing import Type

import pandas as pd

from investd.sources import bonds, bossa, revolut_stocks, xtb
from investd.sources.base import SourceBase
from investd.transaction import Transaction

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
