import pandas as pd

from investd.common import AssetType
from investd.transaction import load_transactions


def test_load_transactions():
    df_tx = load_transactions()
    assert df_tx.shape == (19, 12)
    assert df_tx["type"].dtype == pd.CategoricalDtype(
        categories=[
            AssetType.Stock,
            AssetType.ETF,
            AssetType.Crypto,
            AssetType.FX,
            AssetType.Bond,
        ]
    )
    assert df_tx["timestamp"].dtype == "datetime64[ns]"
