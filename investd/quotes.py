from datetime import date
from typing import Iterable

import pandas as pd
import yfinance

from .config import PERSIST_PATH
from .transaction import load_transactions

SYMBOL_SUFFIX_ADJUST = {"FR": "PA", "UK": "L", "PL": "WA"}


def adjust_symbol(symbol: str) -> str:
    match symbol.split("."):
        case main_part, suffix:
            return f"{main_part}.{SYMBOL_SUFFIX_ADJUST.get(suffix, suffix)}"
        case _:
            return symbol


def fetch_quotes(
    symbols: Iterable[str], from_date: date, until_date: date
) -> pd.DataFrame:
    return yfinance.download(
        " ".join(map(adjust_symbol, symbols)),
        start=from_date,
        end=until_date,
        groupby="ticker",
    )


def generate_quotes_csv() -> None:
    df_tx = load_transactions()
    symbols = df_tx["symbol"].unique()
    earliest_transaction = df_tx["timestamp"].min()
    today = date.today()
    df_quotes = fetch_quotes(symbols, earliest_transaction, today)
    df_quotes.to_csv(PERSIST_PATH / "quotes.csv")
