import pandas as pd

from investd.common import Action, AssetType
from investd.transaction import load_transactions


def test_load_transactions():
    df_tx = load_transactions()
    assert df_tx.shape == (19, 12)
    assert df_tx["timestamp"].dtype == "datetime64[ns]"
    assert df_tx["type"].dtype == pd.CategoricalDtype(
        categories=[
            AssetType.Stock,
            AssetType.ETF,
            AssetType.Crypto,
            AssetType.FX,
            AssetType.Bond,
        ]
    )
    assert set(df_tx["type"]) == {AssetType.Stock, AssetType.ETF}
    assert set(df_tx["action"].unique()) == {Action.BUY, Action.SELL}
