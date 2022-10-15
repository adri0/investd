"""
    Portfolio metrics

    Functions for calculating portfolio metrics, such as net worth, etc.
"""

import pandas as pd

from .model import Action


def signed_ref_amount(df_tx: pd.DataFrame) -> pd.DataFrame:
    """
    Add 'signed_ref_amount' col to dataframe corresponding to
    negative sign to amount_ref_currency when action SELL.
    """
    if "signed_ref_amount" in df_tx.columns:
        return df_tx

    def get_signed_amount(row) -> float:
        return row["amount_ref_currency"] * (-1 if row["action"] == Action.SELL else 1)

    df_tx["signed_ref_amount"] = df_tx.apply(get_signed_amount, axis=1)
    return df_tx


def total_invested(df_tx: pd.DataFrame) -> float:
    """
    Calculates total invested amount in the reference currency.
    """
    df_tx = signed_ref_amount(df_tx)
    return df_tx["signed_ref_amount"].sum()


def invested_amount_by_col(df_tx: pd.DataFrame, col: str) -> pd.Series:
    """
    Generates a Series with invested amount by asset type in the reference currency.
    """
    df_tx = signed_ref_amount(df_tx)
    return df_tx.groupby(col)["signed_ref_amount"].sum()
