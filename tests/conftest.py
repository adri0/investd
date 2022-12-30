from pathlib import Path

import pandas as pd
import pytest

from investd.config import SOURCE_BASE_PATH
from investd.model import Action, AssetType, Currency


@pytest.fixture
def path_resources() -> Path:
    return Path(__file__).parent / "resources"


@pytest.fixture
def cleanup_reports(path_resources):
    yield
    for path in (path_resources / "data/reports").glob("*.html"):
        path.unlink()


@pytest.fixture
def path_revolut_csv() -> Path:
    return SOURCE_BASE_PATH / "revolut_stocks/revolut-stocks-statement.csv"


@pytest.fixture
def path_xtb_xlsx() -> Path:
    return SOURCE_BASE_PATH / "xtb/xtb-statement.xlsx"


@pytest.fixture
def path_xtb_csv() -> Path:
    return SOURCE_BASE_PATH / "xtb/xtb-statement.csv"


@pytest.fixture
def path_bonds_xls() -> Path:
    return SOURCE_BASE_PATH / "bonds/bonds-statement.xls"


@pytest.fixture
def path_bossa_csv() -> Path:
    return SOURCE_BASE_PATH / "bossa/bossa-statement.csv"


@pytest.fixture
def df_tx_minimal() -> pd.DataFrame:
    df_tx = pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "timestamp": ["2021-12-01", "2022-01-01", "2022-01-30", "2022-02-01"],
            "symbol": ["LOL", "TLDR", "XOXO", "LOL"],
            "type": [AssetType.Stock, AssetType.Stock, AssetType.ETF, AssetType.Stock],
            "platform": ["revolut_stocks", "revolut_stocks", "xtb", "revolut_stocks"],
            "currency": [Currency.USD, Currency.USD, Currency.EUR, Currency.USD],
            "amount": [100.0, 150.0, 300.0, 60.0],
            "quantity": [2, 6, 2, 1],
            "price": [50, 25, 150, 60],
            "exchange_rate": [4.5, 4.5, 5.0, 4.6],
            "amount_ref_currency": [450, 675, 1500, 276],
            "action": [Action.BUY, Action.BUY, Action.BUY, Action.SELL],
        }
    )
    categories = ("type", "platform", "currency", "action")
    for cat in categories:
        df_tx[cat] = df_tx[cat].astype("category")
    df_tx["timestamp"] = df_tx["timestamp"].astype("datetime64")
    return df_tx
