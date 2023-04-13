from datetime import date
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
import yfinance

from investd.config import INVESTD_PERSIST
from investd.transaction import load_transactions

QUOTES_FILENAME = "quotes.csv"
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
        tickers=" ".join(sorted(symbols)),
        start=from_date,
        end=until_date,
        group_by="ticker",
    )


def download_quotes_to_csv(
    output_path: Optional[Path] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    symbols: Optional[Iterable[str]] = None,
) -> None:
    df_tx = load_transactions()
    symbols = symbols or df_tx["symbol"].unique()
    adjusted_symbol_to_symbol = {adjust_symbol(symbol): symbol for symbol in symbols}
    df_quotes = fetch_quotes(
        symbols=adjusted_symbol_to_symbol.keys(),
        from_date=start_date or df_tx["timestamp"].min().date(),
        until_date=end_date or date.today(),
    )

    # transform yfinance table to simpler format
    df = pd.DataFrame.from_dict(
        {
            symbol: df_quotes.loc[:, (symbol, "Close")]
            for symbol in adjusted_symbol_to_symbol.keys()
            if symbol
        }
    )
    df["date"] = df_quotes.index.date
    df = df.melt(
        id_vars=["date"], value_vars=df.columns, var_name="symbol", value_name="price"
    )
    df = df.sort_values(["date", "symbol"])

    df.to_csv(output_path or INVESTD_PERSIST / QUOTES_FILENAME, index=False)


def load_quotes() -> pd.DataFrame:
    df_quotes = pd.read_csv(INVESTD_PERSIST / QUOTES_FILENAME)
    df_quotes["date"] = df_quotes["date"].map(lambda dt: pd.to_datetime(dt).date())
    return df_quotes
