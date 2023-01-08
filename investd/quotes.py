from datetime import date
from pathlib import Path
from typing import Iterable, Optional

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
        tickers=" ".join(map(adjust_symbol, symbols)),
        start=from_date,
        end=until_date,
        group_by="ticker",
    )


def generate_quotes_csv(
    output_path: Optional[Path] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    symbols: Optional[Iterable[str]] = [],
) -> None:
    df_tx = load_transactions()
    df_quotes = fetch_quotes(
        symbols=symbols or df_tx["symbol"].unique(),
        from_date=start_date or df_tx["timestamp"].min().date(),
        until_date=end_date or date.today(),
    )
    df_quotes.to_csv(output_path or PERSIST_PATH / "quotes.csv")


def load_quotes() -> pd.DataFrame:
    df_quotes = pd.read_csv(PERSIST_PATH / "quotes.csv", header=[0, 1, 2], index_col=0)
    df_quotes.index = df_quotes.index.map(lambda dt: pd.to_datetime(dt).date())
    return df_quotes
