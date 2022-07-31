from datetime import datetime
from locale import currency
from re import S
from typing import Iterator

import pandas as pd

from .model import AssetInvested, Portfolio, Transaction


def get_portfolio_state(tx: Iterator[Transaction], when: datetime=None) -> Portfolio:
    df_tx = pd.DataFrame(tx)
    portfolio = Portfolio(
        to_date=when,
        total_invested=df_tx["Amount"].sum()
    )
    return portfolio


def get_state(tx: Iterator[Transaction]) -> Iterator[AssetInvested]:
    df_tx = pd.DataFrame(tx)
    df_agg = df_tx.groupby("symbol").aggregate({
        "symbol": "first",
        "currency": "first",
        "quantity": "quantity",
        "amount": "sum",
        "amount_ref_currency": "sum"
    })
    return df_agg