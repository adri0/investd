from datetime import date
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
import yfinance

from investd.common import Currency
from investd.config import INVESTD_PERSIST, INVESTD_REF_CURRENCY
from investd.transaction import load_transactions

QUOTES_FILENAME = "quotes.csv"
SYMBOL_EXCH_ADJUST = {"FR": "PA", "UK": "L", "PL": "WA"}
SYMBOL_NAME_ADJUST = {"DAXEX": "EXS1"}


def adjust_symbol(symbol: str) -> str:
    """Adjust symbol to match how it's used by yfinance"""
    match symbol.split("."):
        case name, exchange:
            name = SYMBOL_NAME_ADJUST.get(name, name)
            exchange = SYMBOL_EXCH_ADJUST.get(exchange, exchange)
            return f"{name}.{exchange}"
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
        interval="1d",
    )


def download_quotes_to_csv(
    output_path: Optional[Path] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    symbols: Optional[list[str]] = None,
    include_exchange_rates: Optional[bool] = False,
) -> None:
    df_tx = load_transactions()
    symbols_selected = symbols or list(df_tx["symbol"].unique())

    # If `symbols` is specified, `include_exchange_rates` is ignored
    if not symbols and include_exchange_rates:
        exchange_rate_symbols = extract_exchange_rates_symbols(df_tx)
        symbols_selected += exchange_rate_symbols

    adjusted_symbol_to_symbol = {
        adjust_symbol(symbol): symbol for symbol in symbols_selected
    }
    df_quotes = fetch_quotes(
        symbols=adjusted_symbol_to_symbol.keys(),
        from_date=start_date or df_tx["timestamp"].min().date(),
        until_date=end_date or date.today(),
    )

    # transform yfinance table to simpler format
    df = pd.DataFrame.from_dict(
        {
            symbol: df_quotes.loc[:, (adj_symbol, "Close")]
            for adj_symbol, symbol in adjusted_symbol_to_symbol.items()
            if adj_symbol in df_quotes.columns.get_level_values(0)
        }
    )
    df["date"] = df_quotes.index
    df = df.melt(
        id_vars=["date"], value_vars=df.columns, var_name="symbol", value_name="price"
    )
    df = df.sort_values(["date", "symbol"])

    df.to_csv(output_path or INVESTD_PERSIST / QUOTES_FILENAME, index=False)


def load_quotes() -> pd.DataFrame:
    return pd.read_csv(INVESTD_PERSIST / QUOTES_FILENAME, parse_dates=["date"])


def extract_exchange_rates_symbols(
    df_tx: pd.DataFrame, ref_currency: Optional[Currency] = None
) -> set[str]:
    ref_currency = ref_currency or INVESTD_REF_CURRENCY
    return {
        f"{cur}{ref_currency}=X"
        for cur in df_tx["currency"].unique()
        if cur != ref_currency
    }
