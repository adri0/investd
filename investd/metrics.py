"""
    Portfolio metrics

    Functions for calculating portfolio metrics, such as net worth, etc.
"""

import pandas as pd

from .model import Action


def add_signed_cols(df_tx: pd.DataFrame) -> pd.DataFrame:
    """
    Add columns ending with _signed to dataframe corresponding to
    negative sign to original amount column when action SELL.
    """
    cols = ("amount_ref_currency", "amount")

    def get_signed_amount(row, col: str) -> float:
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
    df_tx = add_signed_cols(df_tx)
    return df_tx["amount_ref_currency_signed"].sum()


def invested_ref_amount_by_col(df_tx: pd.DataFrame, col: str) -> pd.Series:
    """
    Generates a Series with invested amount by asset type in the reference currency.
    """
    df_tx = add_signed_cols(df_tx)
    return df_tx.groupby(col)["amount_ref_currency_signed"].sum()


def invested_amount_original_currency_by_col(
    df_tx: pd.DataFrame, col: str
) -> pd.core.generic.NDFrame:
    """
    Agregate invested amount by currency.
    """
    df_tx = add_signed_cols(df_tx)
    grouping: list[str] | str = ["currency", col] if col != "currency" else col
    return df_tx.groupby(grouping)["amount_signed"].sum()
