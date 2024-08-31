"""
Portfolio metrics

Functions for calculating portfolio metrics, such as net worth, etc.
"""

from datetime import date
from typing import Any, Iterable

import pandas as pd

from investd import config
from investd.common import Action


def _add_signed_cols(df_tx: pd.DataFrame) -> pd.DataFrame:
    """
    Add columns ending with _signed to dataframe corresponding to
    negative sign to original amount column when action SELL.
    """
    cols = ("amount_ref_currency", "amount", "quantity")

    def get_signed_amount(row: pd.Series, col: str) -> float:
        return row[col] * (-1 if row["action"] == Action.SELL else 1)

    for col in cols:
        signed_col_name = col + "_signed"
        if signed_col_name in df_tx.columns:
            continue
        df_tx[signed_col_name] = df_tx.apply(get_signed_amount, axis=1, args=(col,))
    return df_tx


def total_invested_ref_currency(df_tx: pd.DataFrame) -> float:
    """
    Calculates total invested amount in the reference currency.
    """
    df_tx = _add_signed_cols(df_tx)
    return df_tx["amount_ref_currency_signed"].sum()


def to_nice_df(ndf: pd.DataFrame | pd.Series, columns: Iterable[str]) -> pd.DataFrame:
    """Transforms series into a nice looking dataframe in a notebook."""
    df = pd.DataFrame(ndf)
    df = df.map(round, ndigits=2)  # type: ignore
    df.columns = pd.Index(columns).map(str)
    df.index.set_names(None, inplace=True)
    return df


def add_pct_col(
    df: pd.DataFrame, based_on_col: Any, pct_col_name: str = "%"
) -> pd.DataFrame:
    """Adds percentage column to dataframe."""
    df[pct_col_name] = round(df[based_on_col] / df[based_on_col].sum() * 100, ndigits=1)
    return df


def invested_ref_amount_by_col(df_tx: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Generates a Series with invested amount by asset type in the reference currency.
    """
    df_tx = _add_signed_cols(df_tx)
    grouped = df_tx.groupby(col, observed=False)["amount_ref_currency_signed"].sum()
    ref_currency = config.INVESTD_REF_CURRENCY
    df = to_nice_df(grouped, columns=[str(ref_currency)])
    df = add_pct_col(df, based_on_col=str(ref_currency))
    return df


def amounts_by_currency(df_tx: pd.DataFrame) -> pd.DataFrame:
    """
    Amounts aggregated by currency, showing invested amounts in
    original currency and reference currency.
    """
    df_tx = _add_signed_cols(df_tx)
    df_cur = df_tx.groupby("currency", observed=False)[
        ["amount_signed", "amount_ref_currency_signed"]
    ].sum()
    ref_currency = config.INVESTD_REF_CURRENCY
    df_cur = to_nice_df(df_cur, columns=["Original currency", str(ref_currency)])
    df_cur = add_pct_col(df_cur, str(ref_currency))
    return df_cur


def invested_amount_original_cur_by_col(
    df_tx: pd.DataFrame, col: str
) -> pd.DataFrame | pd.Series:
    """
    Aggregate invested amount by currency.
    """
    df_tx = _add_signed_cols(df_tx)
    grouping: list[str] | str = ["currency", col] if col != "currency" else col
    return df_tx.groupby(grouping, observed=False)["amount_signed"].sum()


def amount_over_time(df_tx: pd.DataFrame, period: str) -> pd.DataFrame:
    """
    Amounts aggregate by periods over time.
    """
    df_tx = _add_signed_cols(df_tx)
    df_ot = (
        df_tx[["timestamp", "amount_ref_currency_signed"]]
        .groupby(pd.Grouper(key="timestamp", freq=period))
        .sum()
    )
    df_ot.index = df_ot.index.to_period()  # type: ignore
    df_ot["cumsum"] = df_ot["amount_ref_currency_signed"].cumsum()
    ref_currency = config.INVESTD_REF_CURRENCY
    df_ot = to_nice_df(df_ot, columns=[str(ref_currency), f"Cumulated {ref_currency}"])
    return df_ot


def portfolio_value(
    df_tx: pd.DataFrame, df_quotes: pd.DataFrame, at_date: date
) -> pd.DataFrame:
    df_tx = _add_signed_cols(df_tx)
    at_date_ts = pd.Timestamp(at_date)
    df_tx = df_tx[df_tx["timestamp"] <= at_date_ts]
    df_portfolio = df_tx.groupby("symbol").agg(
        {
            "amount_ref_currency_signed": "sum",
            "amount_signed": "sum",
            "quantity_signed": "sum",
            "type": "first",
            "currency": "first",
            "platform": "first",
        }
    )
    df_quotes_date = df_quotes[df_quotes["date"] == at_date_ts]
    quotes = df_quotes_date.set_index("symbol")["price"]
    df_portfolio["quote"] = df_portfolio.index.map(quotes)
    df_portfolio["amount_at_date"] = (
        df_portfolio["quote"] * df_portfolio["quantity_signed"]
    )
    ref_currency = config.INVESTD_REF_CURRENCY
    exchange_rate_to_ref_cur = (
        df_portfolio["currency"]
        .map(
            lambda cur: quotes.get(f"{cur}{ref_currency}=X")
            if cur != ref_currency
            else 1
        )
        .astype(float)
    )
    df_portfolio["amount_ref_currency_at_date"] = (
        df_portfolio["amount_at_date"] * exchange_rate_to_ref_cur
    )
    df_portfolio = df_portfolio.rename(
        {
            "amount_at_date": "Amount at date",
            "amount_ref_currency_at_date": f"Amount at date {ref_currency}",
            "amount_signed": "Invested amount",
            "amount_ref_currency_signed": f"Invested amount {ref_currency}",
            "quantity_signed": "Quantity",
        },
        axis=1,
    )
    return df_portfolio
